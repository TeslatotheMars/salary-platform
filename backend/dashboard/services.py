from django.core.cache import cache
from .filters import build_where, normalize_key
from .privacy import suppress_if_small
from .sql import fetch_one, fetch_all

def _count(where_sql: str, args: list) -> int:
    row = fetch_one(f"SELECT COUNT(*) FROM records_salaryrecord r WHERE {where_sql}", args)
    return int(row[0]) if row else 0

def summary(params):
    where_sql, args = build_where(params)
    key = f"dash:summary:{normalize_key(params)}"
    cached = cache.get(key)
    if cached:
        return cached

    cnt = _count(where_sql, args)
    if suppress_if_small(cnt):
        out = {"count": cnt, "suppressed": True}
        cache.set(key, out, 60)
        return out

    sql = f"""
    SELECT
      AVG(r.salary_eur)::float AS mean,
      MIN(r.salary_eur)::float AS min,
      MAX(r.salary_eur)::float AS max,
      percentile_cont(0.25) WITHIN GROUP (ORDER BY r.salary_eur)::float AS p25,
      percentile_cont(0.50) WITHIN GROUP (ORDER BY r.salary_eur)::float AS median,
      percentile_cont(0.75) WITHIN GROUP (ORDER BY r.salary_eur)::float AS p75
    FROM records_salaryrecord r
    WHERE {where_sql}
    """
    row = fetch_one(sql, args)
    out = {
        "count": cnt,
        "suppressed": False,
        "mean": row[0],
        "min": row[1],
        "max": row[2],
        "p25": row[3],
        "median": row[4],
        "p75": row[5],
    }
    cache.set(key, out, 60)
    return out

def options(params):
    where_sql, args = build_where(params)
    key = f"dash:options:{normalize_key(params)}"
    cached = cache.get(key)
    if cached:
        return cached

    def distinct(col):
        rows = fetch_all(
            f"SELECT DISTINCT {col} FROM records_salaryrecord r WHERE {where_sql} ORDER BY {col} LIMIT 5000",
            args,
        )
        return [r[0] for r in rows if r and r[0] is not None]

    out = {
        "cities": distinct("r.city"),
        "industries": distinct("r.industry"),
        "occupations": distinct("r.occupation"),
        "majors": distinct("r.major"),
        "universities": distinct("r.university"),
        "experience_categories": distinct("r.experience_category"),
    }
    cache.set(key, out, 300)
    return out

def grouped(params, group_by: str, metric: str = "median", limit: int = 20):
    allowed = {
        "city": "r.city",
        "industry": "r.industry",
        "occupation": "r.occupation",
        "major": "r.major",
        "university": "r.university",
        "experience_category": "r.experience_category",
    }
    if group_by not in allowed:
        raise ValueError("invalid group_by")

    where_sql, args = build_where(params)
    key = f"dash:grouped:{group_by}:{metric}:{limit}:{normalize_key(params)}"
    cached = cache.get(key)
    if cached:
        return cached

    cnt = _count(where_sql, args)
    if suppress_if_small(cnt):
        out = {"count": cnt, "suppressed": True, "data": []}
        cache.set(key, out, 60)
        return out

    if metric == "mean":
        metric_sql = "AVG(r.salary_eur)::float"
    else:
        metric_sql = "percentile_cont(0.50) WITHIN GROUP (ORDER BY r.salary_eur)::float"

    sql = f"""
    SELECT {allowed[group_by]} AS key,
           {metric_sql} AS value,
           COUNT(*)::int AS n
    FROM records_salaryrecord r
    WHERE {where_sql}
    GROUP BY {allowed[group_by]}
    ORDER BY value DESC NULLS LAST
    LIMIT %s
    """
    rows = fetch_all(sql, args + [limit])
    out = {
        "count": cnt,
        "suppressed": False,
        "data": [{"key": r[0], "value": r[1], "n": r[2]} for r in rows],
    }
    cache.set(key, out, 60)
    return out

def distribution(params, bins: int = 20):
    where_sql, args = build_where(params)
    key = f"dash:dist:{bins}:{normalize_key(params)}"
    cached = cache.get(key)
    if cached:
        return cached

    cnt = _count(where_sql, args)
    if suppress_if_small(cnt):
        out = {"count": cnt, "suppressed": True, "bins": [], "counts": []}
        cache.set(key, out, 60)
        return out

    mm = fetch_one(
        f"SELECT MIN(r.salary_eur)::float, MAX(r.salary_eur)::float FROM records_salaryrecord r WHERE {where_sql}",
        args
    )
    minv, maxv = float(mm[0]), float(mm[1])
    if minv == maxv:
        out = {"count": cnt, "suppressed": False, "bins": [minv], "counts": [cnt]}
        cache.set(key, out, 60)
        return out

    sql = f"""
    SELECT bucket, COUNT(*)::int
    FROM (
      SELECT width_bucket(r.salary_eur, %s, %s, %s) AS bucket
      FROM records_salaryrecord r
      WHERE {where_sql}
    ) t
    GROUP BY bucket
    ORDER BY bucket
    """
    rows = fetch_all(sql, [minv, maxv, bins] + args)
    step = (maxv - minv) / bins
    bin_edges = [minv + step * i for i in range(bins + 1)]
    counts = [0] * bins
    for b, c in rows:
        if b is None:
            continue
        idx = int(b) - 1
        if 0 <= idx < bins:
            counts[idx] = c
    out = {"count": cnt, "suppressed": False, "bins": bin_edges, "counts": counts}
    cache.set(key, out, 60)
    return out

def compare(params, a_prefix="a_", b_prefix="b_"):
    class PWrap:
        def __init__(self, qp, prefix):
            self.qp = qp
            self.prefix = prefix
        def getlist(self, key):
            return self.qp.getlist(self.prefix + key)

    a = summary(PWrap(params, a_prefix))
    b = summary(PWrap(params, b_prefix))

    delta = {}
    if not a.get("suppressed") and not b.get("suppressed"):
        for k in ("median","p25","p75","mean"):
            if a.get(k) is not None and b.get(k) is not None:
                delta[k] = a[k] - b[k]
    return {"a": a, "b": b, "delta": delta}

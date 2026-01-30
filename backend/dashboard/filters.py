ALLOWED_FILTERS = {
    "city": "r.city",
    "industry": "r.industry",
    "occupation": "r.occupation",
    "major": "r.major",
    "university": "r.university",
    "experience_category": "r.experience_category",
}

def build_where(params):
    clauses = ["r.deleted_at IS NULL"]
    values = []
    for key, col in ALLOWED_FILTERS.items():
        vals = params.getlist(key)
        vals = [v.strip() for v in vals if v and v.strip()]
        if vals:
            placeholders = ",".join(["%s"] * len(vals))
            clauses.append(f"{col} IN ({placeholders})")
            values.extend(vals)
    return " AND ".join(clauses), values

def normalize_key(params) -> str:
    parts=[]
    for key in sorted(ALLOWED_FILTERS.keys()):
        vals = sorted([v.strip() for v in params.getlist(key) if v and v.strip()])
        if vals:
            parts.append(f"{key}=" + "|".join(vals))
    return "&".join(parts) if parts else "all"

import * as React from "react";
import MultiSelect from "../components/MultiSelect";
import { api } from "../lib/api";
import { Button } from "../components/ui/button";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

type Filters = {
  city: string[];
  industry: string[];
  occupation: string[];
  major: string[];
  university: string[];
  experience_category: string[];
};

function toQS(filters: Filters) {
  const p = new URLSearchParams();
  (Object.keys(filters) as (keyof Filters)[]).forEach((k) => {
    filters[k].forEach((v) => p.append(k, v));
  });
  return p.toString();
}

function Kpi({ label, value }: { label: string; value: any }) {
  return (
    <div className="rounded-lg border border-black/10 bg-white p-3">
      <div className="text-xs text-black/60">{label}</div>
      <div className="mt-1 text-xl font-semibold">{value ?? "—"}</div>
    </div>
  );
}

export default function DashboardPage() {
  const [mode, setMode] = React.useState<"explore"|"compare">("explore");
  const [filters, setFilters] = React.useState<Filters>({
    city: [], industry: [], occupation: [], major: [], university: [], experience_category: []
  });

  // compare filters
  const [aFilters, setAFilters] = React.useState<Filters>({ city: [], industry: [], occupation: [], major: [], university: [], experience_category: []});
  const [bFilters, setBFilters] = React.useState<Filters>({ city: [], industry: [], occupation: [], major: [], university: [], experience_category: []});

  const [options, setOptions] = React.useState<any>(null);
  const [summary, setSummary] = React.useState<any>(null);
  const [grouped, setGrouped] = React.useState<any>(null);
  const [groupBy, setGroupBy] = React.useState<string>("city");
  const [compare, setCompare] = React.useState<any>(null);

  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string>("");

  const qs = toQS(filters);

  React.useEffect(() => {
    let alive = true;
    setLoading(true);
    setError("");
    Promise.all([
      api.options(qs),
      api.summary(qs),
      api.grouped(new URLSearchParams({ ...Object.fromEntries(new URLSearchParams(qs)), group_by: groupBy, metric: "median", limit: "20" } as any).toString()),
    ]).then(([o, s, g]) => {
      if (!alive) return;
      setOptions(o);
      setSummary(s);
      setGrouped(g);
    }).catch((e) => {
      if (!alive) return;
      setError(e.message || "Failed to load");
    }).finally(() => alive && setLoading(false));
    return () => { alive = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [qs, groupBy]);

  async function loadCompare() {
    setLoading(true);
    setError("");
    try {
      const p = new URLSearchParams();
      (Object.keys(aFilters) as (keyof Filters)[]).forEach((k) => aFilters[k].forEach(v => p.append("a_"+k, v)));
      (Object.keys(bFilters) as (keyof Filters)[]).forEach((k) => bFilters[k].forEach(v => p.append("b_"+k, v)));
      const data = await api.compare(p.toString());
      setCompare(data);
    } catch (e: any) {
      setError(e.message || "Failed to compare");
    } finally {
      setLoading(false);
    }
  }

  const suppressed = summary?.suppressed;

  return (
    <div className="mx-auto max-w-6xl px-4 py-6">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <div className="text-2xl font-semibold">Dashboard</div>
          <div className="text-sm text-black/60">Aggregated only · k=5 suppression · EUR</div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant={mode==="explore" ? "default" : "outline"} onClick={() => setMode("explore")}>Explore</Button>
          <Button variant={mode==="compare" ? "default" : "outline"} onClick={() => setMode("compare")}>Compare</Button>
        </div>
      </div>

      {error ? <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm">{error}</div> : null}
      {loading ? <div className="mb-4 text-sm text-black/60">Loading…</div> : null}

      {mode === "explore" ? (
        <>
          <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
            <MultiSelect label="City" options={options?.cities || []} value={filters.city} onChange={(v) => setFilters({ ...filters, city: v })} />
            <MultiSelect label="Industry" options={options?.industries || []} value={filters.industry} onChange={(v) => setFilters({ ...filters, industry: v })} />
            <MultiSelect label="Occupation" options={options?.occupations || []} value={filters.occupation} onChange={(v) => setFilters({ ...filters, occupation: v })} />
            <MultiSelect label="Major" options={options?.majors || []} value={filters.major} onChange={(v) => setFilters({ ...filters, major: v })} />
            <MultiSelect label="University" options={options?.universities || []} value={filters.university} onChange={(v) => setFilters({ ...filters, university: v })} />
            <MultiSelect label="Experience" options={options?.experience_categories || []} value={filters.experience_category} onChange={(v) => setFilters({ ...filters, experience_category: v })} />
          </div>

          <div className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-4">
            <Kpi label="Count" value={summary?.count ?? "—"} />
            <Kpi label="Median" value={suppressed ? "—" : summary?.median?.toFixed?.(0)} />
            <Kpi label="P25" value={suppressed ? "—" : summary?.p25?.toFixed?.(0)} />
            <Kpi label="P75" value={suppressed ? "—" : summary?.p75?.toFixed?.(0)} />
          </div>

          {suppressed ? (
            <div className="mt-4 rounded-lg border border-black/10 bg-black/5 p-4 text-sm">
              Sample size is too small (k=5). Charts and detailed stats are suppressed.
            </div>
          ) : (
            <div className="mt-6 rounded-lg border border-black/10 bg-white p-4">
              <div className="mb-3 flex items-center justify-between">
                <div className="font-medium">Top groups by median salary</div>
                <select
                  className="h-9 rounded-md border border-black/20 bg-white px-2 text-sm"
                  value={groupBy}
                  onChange={(e) => setGroupBy(e.target.value)}
                >
                  <option value="city">city</option>
                  <option value="industry">industry</option>
                  <option value="occupation">occupation</option>
                  <option value="major">major</option>
                  <option value="university">university</option>
                  <option value="experience_category">experience</option>
                </select>
              </div>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={(grouped?.data || []).map((d: any) => ({ name: d.key, value: d.value }))}>
                    <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                    <YAxis tick={{ fontSize: 12 }} />
                    <Tooltip />
                    <Bar dataKey="value" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </>
      ) : (
        <>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div className="rounded-lg border border-black/10 bg-white p-4">
              <div className="mb-2 font-medium">Group A</div>
              <div className="grid grid-cols-1 gap-3">
                <MultiSelect label="City" options={options?.cities || []} value={aFilters.city} onChange={(v) => setAFilters({ ...aFilters, city: v })} />
                <MultiSelect label="Industry" options={options?.industries || []} value={aFilters.industry} onChange={(v) => setAFilters({ ...aFilters, industry: v })} />
                <MultiSelect label="Occupation" options={options?.occupations || []} value={aFilters.occupation} onChange={(v) => setAFilters({ ...aFilters, occupation: v })} />
                <MultiSelect label="Experience" options={options?.experience_categories || []} value={aFilters.experience_category} onChange={(v) => setAFilters({ ...aFilters, experience_category: v })} />
              </div>
            </div>

            <div className="rounded-lg border border-black/10 bg-white p-4">
              <div className="mb-2 font-medium">Group B</div>
              <div className="grid grid-cols-1 gap-3">
                <MultiSelect label="City" options={options?.cities || []} value={bFilters.city} onChange={(v) => setBFilters({ ...bFilters, city: v })} />
                <MultiSelect label="Industry" options={options?.industries || []} value={bFilters.industry} onChange={(v) => setBFilters({ ...bFilters, industry: v })} />
                <MultiSelect label="Occupation" options={options?.occupations || []} value={bFilters.occupation} onChange={(v) => setBFilters({ ...bFilters, occupation: v })} />
                <MultiSelect label="Experience" options={options?.experience_categories || []} value={bFilters.experience_category} onChange={(v) => setBFilters({ ...bFilters, experience_category: v })} />
              </div>
            </div>
          </div>

          <div className="mt-4">
            <Button onClick={loadCompare}>Run Compare</Button>
          </div>

          {compare ? (
            <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-3">
              <div className="rounded-lg border border-black/10 bg-white p-4">
                <div className="font-medium">A</div>
                <div className="mt-2 text-sm text-black/70">count: {compare.a.count}</div>
                <div className="text-sm text-black/70">median: {compare.a.suppressed ? "—" : compare.a.median?.toFixed?.(0)}</div>
              </div>
              <div className="rounded-lg border border-black/10 bg-white p-4">
                <div className="font-medium">B</div>
                <div className="mt-2 text-sm text-black/70">count: {compare.b.count}</div>
                <div className="text-sm text-black/70">median: {compare.b.suppressed ? "—" : compare.b.median?.toFixed?.(0)}</div>
              </div>
              <div className="rounded-lg border border-black/10 bg-white p-4">
                <div className="font-medium">Δ (A - B)</div>
                <div className="mt-2 text-sm text-black/70">median: {compare.delta?.median?.toFixed?.(0) ?? "—"}</div>
              </div>
            </div>
          ) : null}
        </>
      )}
    </div>
  );
}

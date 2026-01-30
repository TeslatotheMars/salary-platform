import * as React from "react";
import { api } from "../lib/api";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Dialog, DialogContent } from "../components/ui/dialog";

const EXPERIENCE = ["under 1 year","1-3 years","3-5 years","5-10 years","above 10 years"];

export default function MySubmissionsPage() {
  const [me, setMe] = React.useState<any>(null);
  const [data, setData] = React.useState<any>(null);
  const [err, setErr] = React.useState("");
  const [open, setOpen] = React.useState(false);

  const [form, setForm] = React.useState({
    university: "",
    major: "",
    industry: "",
    occupation: "",
    experience_category: "1-3 years",
    city: "",
    salary_eur: ""
  });

  async function refresh() {
    setErr("");
    try {
      const m = await api.me();
      const r = await api.mySubmissions(m.year);
      setMe(m);
      setData(r);
    } catch (e: any) {
      setErr(e.message || "Failed");
    }
  }

  React.useEffect(() => { refresh(); }, []);

  async function submit() {
    setErr("");
    try {
      await api.submitRecord({
        ...form,
        salary_eur: Number(form.salary_eur)
      });
      setOpen(false);
      setForm({ university:"", major:"", industry:"", occupation:"", experience_category:"1-3 years", city:"", salary_eur:"" });
      await refresh();
    } catch (e: any) {
      setErr(e.data?.message || e.message || "Submit failed");
    }
  }

  async function del(recordId: number) {
    if (!confirm("Delete this record?")) return;
    setErr("");
    try {
      await api.deleteMyRecord(recordId);
      await refresh();
    } catch (e: any) {
      setErr(e.message || "Delete failed");
    }
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-6">
      <div className="text-2xl font-semibold">My Submissions</div>
      <div className="mt-1 text-sm text-black/60">You can submit at most 2 records per calendar year.</div>

      {err ? <div className="mt-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm">{err}</div> : null}

      <div className="mt-4 flex items-center justify-between rounded-lg border border-black/10 bg-white p-4">
        <div>
          <div className="text-sm text-black/70">Year: {me?.year ?? "—"}</div>
          <div className="text-sm text-black/70">Submitted: {me?.submissions_this_year ?? "—"} / 2</div>
        </div>
        <Button onClick={() => setOpen(true)} disabled={me && me.remaining_this_year <= 0}>
          Submit Salary
        </Button>
      </div>

      <div className="mt-4 rounded-lg border border-black/10 bg-white p-4">
        <div className="font-medium">Records</div>
        <div className="mt-3 overflow-auto">
          <table className="w-full text-sm">
            <thead className="text-left text-black/60">
              <tr>
                <th className="py-2">record_id</th>
                <th>city</th>
                <th>industry</th>
                <th>occupation</th>
                <th>experience</th>
                <th>salary (EUR)</th>
                <th>submission</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {(data?.results || []).map((r: any) => (
                <tr key={r.record_id} className="border-t border-black/5">
                  <td className="py-2">{r.record_id}</td>
                  <td>{r.city}</td>
                  <td>{r.industry}</td>
                  <td>{r.occupation}</td>
                  <td>{r.experience_category}</td>
                  <td>{Number(r.salary_eur).toFixed?.(0) ?? r.salary_eur}</td>
                  <td>{new Date(r.submission_date).toLocaleString()}</td>
                  <td className="text-right">
                    <Button variant="destructive" size="sm" onClick={() => del(r.record_id)}>Delete</Button>
                  </td>
                </tr>
              ))}
              {!data?.results?.length ? (
                <tr><td className="py-3 text-black/60" colSpan={8}>No records yet.</td></tr>
              ) : null}
            </tbody>
          </table>
        </div>
      </div>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <div className="text-lg font-semibold">Submit Salary</div>
          <div className="mt-1 text-sm text-black/60">One submission = one record. Server sets submission date.</div>

          <div className="mt-4 grid grid-cols-1 gap-3">
            <div>
              <div className="mb-1 text-xs text-black/70">University</div>
              <Input value={form.university} onChange={(e) => setForm({ ...form, university: e.target.value })} />
            </div>
            <div>
              <div className="mb-1 text-xs text-black/70">Major</div>
              <Input value={form.major} onChange={(e) => setForm({ ...form, major: e.target.value })} />
            </div>
            <div>
              <div className="mb-1 text-xs text-black/70">Industry</div>
              <Input value={form.industry} onChange={(e) => setForm({ ...form, industry: e.target.value })} />
            </div>
            <div>
              <div className="mb-1 text-xs text-black/70">Occupation</div>
              <Input value={form.occupation} onChange={(e) => setForm({ ...form, occupation: e.target.value })} />
            </div>
            <div>
              <div className="mb-1 text-xs text-black/70">Experience</div>
              <select
                className="h-9 w-full rounded-md border border-black/20 bg-white px-2 text-sm"
                value={form.experience_category}
                onChange={(e) => setForm({ ...form, experience_category: e.target.value })}
              >
                {EXPERIENCE.map(x => <option key={x} value={x}>{x}</option>)}
              </select>
            </div>
            <div>
              <div className="mb-1 text-xs text-black/70">City</div>
              <Input value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
            </div>
            <div>
              <div className="mb-1 text-xs text-black/70">Salary (EUR)</div>
              <Input type="number" value={form.salary_eur} onChange={(e) => setForm({ ...form, salary_eur: e.target.value })} />
            </div>

            <div className="mt-2 flex justify-end gap-2">
              <Button variant="outline" onClick={() => setOpen(false)}>Cancel</Button>
              <Button onClick={submit}>Submit</Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

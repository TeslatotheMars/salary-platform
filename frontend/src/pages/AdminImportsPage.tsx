import * as React from "react";
import { api } from "../lib/api";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

export default function AdminImportsPage() {
  const [file, setFile] = React.useState<File | null>(null);
  const [imports, setImports] = React.useState<any[]>([]);
  const [err, setErr] = React.useState("");
  const [msg, setMsg] = React.useState("");

  async function load() {
    setErr("");
    try {
      const r = await api.adminImportsList();
      setImports(r.results || []);
    } catch (e: any) {
      setErr(e.message || "Failed to load");
    }
  }

  React.useEffect(() => { load(); }, []);

  async function upload() {
    if (!file) return;
    setErr(""); setMsg("");
    try {
      const res = await api.adminImportCsv(file);
      setMsg(`Imported batch ${res.batch_id} (${res.status})`);
      await load();
    } catch (e: any) {
      setErr(e.message || "Import failed");
    }
  }

  async function delBatch(batchId: number) {
    if (!confirm(`Delete batch ${batchId} (soft-delete its records)?`)) return;
    setErr(""); setMsg("");
    try {
      await api.adminDeleteBatch(batchId);
      setMsg(`Deleted batch ${batchId}`);
      await load();
    } catch (e: any) {
      setErr(e.message || "Delete failed");
    }
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-6">
      <div className="text-2xl font-semibold">Admin · CSV Import</div>
      <div className="mt-1 text-sm text-black/60">Import consumes global user_id. Delete by record_id or batch_id only.</div>

      {err ? <div className="mt-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm">{err}</div> : null}
      {msg ? <div className="mt-4 rounded-lg border border-black/10 bg-black/5 p-3 text-sm">{msg}</div> : null}

      <div className="mt-4 rounded-lg border border-black/10 bg-white p-4">
        <div className="font-medium">Upload CSV</div>
        <div className="mt-3 flex items-center gap-2">
          <Input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          <Button onClick={upload} disabled={!file}>Upload</Button>
        </div>
        <div className="mt-2 text-xs text-black/60">
          Required columns (v1 demo): email, University, Major, Industry, Occupation, Experience, City, Salary, Submission_Date
        </div>
      </div>

      <div className="mt-4 rounded-lg border border-black/10 bg-white p-4">
        <div className="font-medium">Import History</div>
        <div className="mt-3 overflow-auto">
          <table className="w-full text-sm">
            <thead className="text-left text-black/60">
              <tr>
                <th className="py-2">batch_id</th>
                <th>status</th>
                <th>rows</th>
                <th>created</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {imports.map((b) => (
                <tr key={b.batch_id} className="border-t border-black/5">
                  <td className="py-2">{b.batch_id}</td>
                  <td>{b.status}</td>
                  <td>{b.rows_success}/{b.rows_total} (failed {b.rows_failed})</td>
                  <td>{new Date(b.created_at).toLocaleString()}</td>
                  <td className="text-right">
                    <Button variant="destructive" size="sm" onClick={() => delBatch(b.batch_id)}>Delete batch</Button>
                  </td>
                </tr>
              ))}
              {!imports.length ? <tr><td className="py-3 text-black/60" colSpan={5}>No imports.</td></tr> : null}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

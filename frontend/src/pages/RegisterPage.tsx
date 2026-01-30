import * as React from "react";
import { useNavigate, Link } from "react-router-dom";
import { api, saveSession, setTokens } from "../lib/api";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

export default function RegisterPage() {
  const nav = useNavigate();
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [err, setErr] = React.useState("");

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr("");
    try {
      const res = await api.register(email, password);
      setTokens(res.access, res.refresh);
      saveSession({ user_id: res.user_id, role: res.role, email: res.email });
      nav("/");
    } catch (e: any) {
      setErr(e.message || "Register failed");
    }
  }

  return (
    <div className="mx-auto max-w-md px-4 py-10">
      <div className="text-2xl font-semibold">Register</div>
      <div className="mt-1 text-sm text-black/60">Creates a global incremental user_id</div>

      {err ? <div className="mt-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm">{err}</div> : null}

      <form className="mt-6 space-y-3" onSubmit={onSubmit}>
        <div>
          <div className="mb-1 text-xs text-black/70">Email</div>
          <Input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
        </div>
        <div>
          <div className="mb-1 text-xs text-black/70">Password (min 8 chars)</div>
          <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <Button className="w-full" type="submit">Create account</Button>
      </form>

      <div className="mt-4 text-sm text-black/70">
        Already have an account? <Link className="underline" to="/login">Login</Link>
      </div>
    </div>
  );
}

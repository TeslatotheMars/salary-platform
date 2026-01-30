const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

export type Role = "USER" | "ADMIN";

export function getTokens() {
  return {
    access: localStorage.getItem("access") || "",
    refresh: localStorage.getItem("refresh") || ""
  };
}

export function setTokens(access: string, refresh?: string) {
  localStorage.setItem("access", access);
  if (refresh) localStorage.setItem("refresh", refresh);
}

export function clearTokens() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("user_id");
  localStorage.removeItem("role");
  localStorage.removeItem("email");
}

async function request(path: string, opts: RequestInit = {}) {
  const { access } = getTokens();
  const headers: Record<string,string> = {
    "Content-Type": "application/json",
    ...(opts.headers as any)
  };
  if (access) headers["Authorization"] = `Bearer ${access}`;
  const res = await fetch(`${API_BASE}${path}`, { ...opts, headers });
  if (res.status === 204) return null;
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;
  if (!res.ok) {
    throw Object.assign(new Error(data?.message || data?.error || "Request failed"), { status: res.status, data });
  }
  return data;
}

export const api = {
  health: () => request("/health", { method: "GET" }),
  register: (email: string, password: string) => request("/auth/register", { method: "POST", body: JSON.stringify({ email, password }) }),
  login: (email: string, password: string) => request("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  me: () => request("/me", { method: "GET" }),

  // user submissions
  mySubmissions: (year?: number) => request(`/my/submissions${year ? `?year=${year}` : ""}`, { method: "GET" }),
  submitRecord: (payload: any) => request("/my/submissions/submit", { method: "POST", body: JSON.stringify(payload) }),
  deleteMyRecord: (recordId: number) => request(`/my/submissions/${recordId}`, { method: "DELETE" }),

  // dashboard
  options: (qs: string) => request(`/dashboard/options${qs ? `?${qs}` : ""}`, { method: "GET" }),
  summary: (qs: string) => request(`/dashboard/summary${qs ? `?${qs}` : ""}`, { method: "GET" }),
  grouped: (qs: string) => request(`/dashboard/grouped${qs ? `?${qs}` : ""}`, { method: "GET" }),
  distribution: (qs: string) => request(`/dashboard/distribution${qs ? `?${qs}` : ""}`, { method: "GET" }),
  compare: (qs: string) => request(`/dashboard/compare${qs ? `?${qs}` : ""}`, { method: "GET" }),

  // admin
  adminImportsList: () => request("/admin/imports/list", { method: "GET" }),
  adminDeleteRecord: (recordId: number) => request(`/admin/records/${recordId}`, { method: "DELETE" }),
  adminDeleteBatch: (batchId: number) => request(`/admin/imports/${batchId}`, { method: "DELETE" }),
  adminImportCsv: async (file: File) => {
    const { access } = getTokens();
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${API_BASE}/admin/imports`, {
      method: "POST",
      body: form,
      headers: access ? { Authorization: `Bearer ${access}` } : undefined
    });
    const text = await res.text();
    const data = text ? JSON.parse(text) : null;
    if (!res.ok) throw Object.assign(new Error(data?.message || data?.error || "Import failed"), { status: res.status, data });
    return data;
  }
};

export function saveSession(info: { user_id: number; role: Role; email: string }) {
  localStorage.setItem("user_id", String(info.user_id));
  localStorage.setItem("role", info.role);
  localStorage.setItem("email", info.email);
}
export function getSession() {
  return {
    user_id: Number(localStorage.getItem("user_id") || "0"),
    role: (localStorage.getItem("role") as Role) || "",
    email: localStorage.getItem("email") || ""
  };
}

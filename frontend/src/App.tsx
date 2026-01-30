import { BrowserRouter, Routes, Route, Navigate, Link, useNavigate } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import MySubmissionsPage from "./pages/MySubmissionsPage";
import AdminImportsPage from "./pages/AdminImportsPage";
import { getSession, clearTokens } from "./lib/api";
import { Button } from "./components/ui/button";

function TopBar() {
  const nav = useNavigate();
  const s = getSession();

  return (
    <div className="sticky top-0 z-40 border-b border-black/10 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to="/" className="font-semibold">Salary Dashboard</Link>
        <div className="flex items-center gap-2">
          {s.user_id ? (
            <>
              <div className="text-sm text-black/70">{s.email} · {s.role}</div>
              <Link to="/me/submissions"><Button variant="outline">My Submissions</Button></Link>
              {s.role === "ADMIN" ? <Link to="/admin/imports"><Button variant="outline">Admin</Button></Link> : null}
              <Button
                variant="ghost"
                onClick={() => { clearTokens(); nav("/"); }}
              >
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link to="/login"><Button variant="outline">Login</Button></Link>
              <Link to="/register"><Button>Register</Button></Link>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function RequireAuth({ children }: { children: JSX.Element }) {
  const s = getSession();
  if (!s.user_id) return <Navigate to="/login" replace />;
  return children;
}
function RequireAdmin({ children }: { children: JSX.Element }) {
  const s = getSession();
  if (!s.user_id) return <Navigate to="/login" replace />;
  if (s.role !== "ADMIN") return <Navigate to="/" replace />;
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <TopBar />
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/me/submissions" element={<RequireAuth><MySubmissionsPage /></RequireAuth>} />
        <Route path="/admin/imports" element={<RequireAdmin><AdminImportsPage /></RequireAdmin>} />
      </Routes>
    </BrowserRouter>
  );
}

# Salary Platform (Django REST + React) — v1.0

This repo implements the frozen v1.0 spec:
- Global auto-increment `user_id` used everywhere (import consumes IDs too)
- User submits own record via modal form (no user CSV upload)
- Limit: **max 2 records per user_id per calendar year** (Europe/Dublin server time)
- Currency fixed to **EUR** (`salary_eur`)
- Dashboard endpoints are aggregated only + **k=5 suppression**
- Admin CSV import + delete by record_id or batch_id only

## Quick start (Docker)
1) Copy env:
```bash
cp infra/.env.example infra/.env
```

2) Start:
```bash
docker compose -f infra/docker-compose.yml up --build
```

3) Backend API: http://localhost:8000/api/health  
   Frontend: http://localhost:5173

## Local dev (without Docker)
See `docs/LOCAL_DEV.md`.

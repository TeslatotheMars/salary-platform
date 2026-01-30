# Salary Platform (Django REST + React) — v1.0

This project follows a modern, production-oriented full-stack architecture, with a clear separation between frontend, backend services, and data layers.
It is designed to support secure salary analytics, role-based access control, and privacy-preserving data aggregation (k-anonymity).

## 1. Technical Architecture

The system is built as a frontend–backend separated architecture using REST APIs.

### Frontend
- Built with React + Vite for fast development and modern UX
- Uses TanStack Query for API caching, refetching, and debouncing
- Recharts is used for salary distributions and grouped comparisons

### Backend
- Implemented with Django + Django REST Framework
- Clear service separation:
  - Authentication & role-based access control (RBAC)
  - Dashboard analytics services
  - User submission services
  - Admin data import & governance services

### Data Layer
- PostgreSQL for production (native percentile and aggregation support)
- Redis (optional) for caching heavy aggregation queries

### Privacy by Design
- All analytics endpoints enforce k-anonymity (k = 5)
- Aggregated results are suppressed when the sample size is below the threshold

## Functional Architecture

From a business and user-interaction perspective, the system is organized around roles and capabilities, not raw CRUD operations.

### Guest Users
- Can explore aggregated salary insights
- Cannot submit, modify, or view individual records
### Registered Users
- Register and log in using email + password
- Receive a globally unique, auto-incrementing user_id
- Can submit up to two salary records per calendar year
- Can view and delete only their own submissions
### Administrators
- Can bulk-import historical salary data via CSV
- Imported records also consume global user_ids
- Can delete data strictly by record_id or batch_id to prevent accidental mass deletion
### Privacy Enforcement
- All dashboard views (Explore & Compare) are protected by k-anonymity
- If the number of matching records is less than 5, detailed statistics and charts are suppressed

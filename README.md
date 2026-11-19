# 1530_Maintenance_Tracker

Members: Yifei Tian, Bakhtiyor Alimov, Dylan Do, Edward Cho, Akshay Ramkumar

## Project Description

- Maintenance Tracker is a web application that helps tenants and landlords manage apartment maintenance issues in one shared place. Today, many maintenance problems go unreported because each roommate assumes someone else already told the landlord, and the ones that do get reported are scattered across text messages with no clear record of who reported what, when, or what happened next.

- With Maintenance Tracker, a tenant logs into an account linked to their unit and submits a report with a short description and an optional photo. Every tenant in the unit can see all active reports, which prevents duplicate messages and makes sure everyone knows an issue has already been raised. Each report is dated on submission and carries a status, so tenants can follow its progress. The landlord can review incoming reports, update their status as action is taken, and mark them resolved.

## Tech Stack

| Layer                   | Technology           | Justification                                                                                                                         |
| ----------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Language(s)             | Python, JavaScript   | Python will be used for backend functionality while JavaScript will be used for the UI                                                |
| Frontend                | Next.js, React       | Next.js allows us to create reusable components which will be nice if we want to make a different dashboard for tenants and landlords |
| Backend                 | Python               | Our team has most experience using python.                                                                                            |
| Database                | PostgreSQL, Supabase | We want to host our database so our team can access and see data without having to configure a separate database.                     |
| APIs / External Service | FastAPI              | FastAPI will allow us to practice making endpoints and will be easy to divide up services for team members.                           |

## Architecture

### Subsystem Decomposition

![Subsystem Decomposition](docs/subsystem-decomposition.png)

### Deployment Diagram

![Deployment Diagram](docs/deployment-diagram.png)

### Folder Structure

| Folder                       | Subsystem                       | Component                                          | Status      |
| ---------------------------- | ------------------------------- | -------------------------------------------------- | ----------- |
| `frontend/`                  | User Interface                  | Tenant Dashboard, Landlord Dashboard               | Running     |
| `backend/app/auth/`          | Authentication & Access Control | Login, Unit/Property Access                        | Placeholder |
| `backend/app/requests/`      | Request Management              | Request Manager, Status Manager                    | In progress |
| `backend/app/reports/`       | Report Data                     | Maintenance Request, Report History                | In progress |
| `backend/app/notifications/` | Notification                    | New Report Notification, Report Seen Notification  | Placeholder |
| `backend/app/attachments/`   | Attachments & Report Chat       | Photo Attachment, Request Chat                     | Placeholder |
| `docs/`                      | N/A                             | Subsystem-decomposition, deployment-diagram images | N/A         |

`backend/app/main.py` is the FastAPI entry point. Report endpoints are in `backend/app/requests/routes.py`, and database queries are in `backend/app/reports/store.py`. The other subsystem folders are still placeholders.

## Prerequisites

- Python 3.12.4 (tested)
- Node.js v26.10.0 (tested)
- npm 11.19.1 (tested)
- Access to the team's Supabase project
- Git

## Setup and Run

### 1. Clone

```bash
git clone https://github.com/YifeiTi/1530-Maintenance_Tracker.git
cd 1530-Maintenance_Tracker
```

### 2. Environment Variables

The backend connects to the team's Supabase PostgreSQL database through the DATABASE_URL environment variable. Copy backend/.env.example to backend/.env and replace [YOUR-PASSWORD] with the database password (ask a teammate, or reset it in Supabase under Project Settings, Database). Never commit .env; it is gitignored.

If the direct connection fails on your network (IPv6 only), use the Session pooler connection string instead (Supabase: Connect > Session pooler).

### 3. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

## How to Check That It Works

- Backend
  - Open http://localhost:8000/health in your browser. `{"status":"ok"}`
- Frontend
  - Open http://localhost:3000 in your browser. You should see the main page of Maintenance Tracker.
- Database
  - The Supabase project (Maintenance-Tracker) contains the schema tables: properties, units, profiles, maintenance_requests, request_attachments, request_messages. The backend reads DATABASE_URL from backend/.env; with the backend running, open http://localhost:8000/health/db and you should see {"status":"ok"} if the Supabase connection works (otherwise status is "error" with the exception name).

### Tests

```bash
cd backend
pytest
```

## Features

### Submit a maintenance report

Send `POST /reports` with `{"description": "sink is leaking", "unit_id": <unit uuid>}`. A blank description is rejected. A saved report gets status `Submitted` and a submission time set by the server. With the backend running, try it at http://localhost:8000/docs.

### View active reports
Send `GET /reports?unit_id=<unit uuid>` to get every active report for a unit (any status except resolved), newest first. Try it at http://localhost:8000/docs under `GET /reports`.

## What Works So Far

- FastAPI backend starts and the `/health` endpoint responds.
- `POST /reports` rejects a blank description.
- `GET /reports` returns a unit's active reports.
- Next.js frontend starts and shows a basic homepage.
- Supabase project is set up with the initial database schema.
- Backend connects to Supabase through the session pooler (/health/db).

## What Does Not Work Yet

- Frontend-to-backend connection, login, and notifications.
- Saving a report: `POST /reports` does not match the database schema yet (status values, required title and tenant_id).

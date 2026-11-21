# Sprint 5 frontend verification

## Scope

Adds report submission, an active report list, and report details to the Next.js homepage. Requests use `/api/reports` and Next.js forwards them to the existing FastAPI backend. Refs #3, #4, #8, #9, and #11. These stories remain partial until login and server-enforced unit access are implemented.

The database status `open` is displayed as Submitted; `in_progress` is displayed as In progress. No backend/database status values were changed. No landlord role is fabricated or sent by the frontend.

## Verification performed

- `npm test`: 3 frontend tests passed (status labels, timestamp formats, and API error messages).
- `npm run build`: production build passed.
- `python -m pytest -q` in backend: 21 existing tests passed.
- Local integration check: 8 checks passed against a running production Next.js server and the actual FastAPI routes. The report store functions were substituted with in-memory functions, so the check did not require database credentials or write to Supabase.
- The integration check covered homepage rendering, empty list, blank-description 400, successful POST, list after creation, detail fetch, missing-report 404, and malformed-UUID 422.
- Environment: Linux, Node.js v24.22.3, npm 11.19.1, Python 3.12.

Browser visual/interaction testing and a real Supabase round trip still need to be completed. Chromium could not start in this execution environment. The integration check verifies HTTP forwarding, not full browser interaction or database persistence.

## Repeat the isolated proxy check

After installing backend dependencies and running `npm ci` and `npm run build` inside frontend, stop any local servers on ports 8000 and 3000, then run this from the repository root:

```bash
python scripts/check_report_proxy.py
```

The script starts the real FastAPI routes with a temporary in-memory store and a Next.js production server. It refuses to run if either port is already occupied, so it does not send writes to an existing backend. It does not validate SQL or Supabase persistence.

## Manual demo using the team database

1. Start FastAPI using the root README instructions and confirm `/health/db` returns `ok`.
2. Start the frontend using `npm ci` and `npm run dev`; open http://localhost:3000.
3. Enter an existing unit UUID and tenant profile UUID from the team's test data. Select Load active reports.
4. Enter a title and description, then select Submit report. Confirm the success notice, Submitted status, timestamp, and refreshed active list.
5. Open the report from the list and confirm its status, timestamp, and planned-fix note or the no-note message.
6. Use the existing PATCH endpoint in Swagger to add a planned-fix note as documented in the README. Reopen the report to see the updated note.
7. Confirm a failed submission keeps the entered text and displays an error. Use disposable team test records, not private tenant data.

Capture screenshots of the actual working frontend for the sprint document. The local HTTP check is not a replacement for the team's database/browser demo.

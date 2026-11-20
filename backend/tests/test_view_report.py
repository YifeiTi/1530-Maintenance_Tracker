from uuid import UUID

from fastapi.testclient import TestClient

from app.main import app
from app.reports import store

client = TestClient(app)

REPORT_ID = UUID("00000000-0000-0000-0000-000000000001")
REPORT_URL = f"/reports/{REPORT_ID}"


def test_view_report_returns_status_and_planned_fix(monkeypatch):
    report = {
        "id": str(REPORT_ID),
        "status": "in_progress",
        "planned_fix_note": "Plumber coming Monday",
        "submitted_at": "2026-11-19T15:00:00Z",
    }

    def fake_get_report_by_id(report_id):
        assert report_id == REPORT_ID
        return report

    monkeypatch.setattr(store, "get_report_by_id", fake_get_report_by_id)

    response = client.get(REPORT_URL)

    assert response.status_code == 200
    assert response.json() == report


def test_view_report_without_planned_fix_returns_null_note(monkeypatch):
    report = {"id": str(REPORT_ID), "status": "open", "planned_fix_note": None}
    monkeypatch.setattr(store, "get_report_by_id", lambda report_id: report)

    response = client.get(REPORT_URL)

    assert response.status_code == 200
    assert response.json()["planned_fix_note"] is None


def test_view_missing_report_returns_404(monkeypatch):
    monkeypatch.setattr(store, "get_report_by_id", lambda report_id: None)

    response = client.get(REPORT_URL)

    assert response.status_code == 404


def test_view_report_requires_valid_uuid():
    response = client.get("/reports/not-a-uuid")

    assert response.status_code == 422
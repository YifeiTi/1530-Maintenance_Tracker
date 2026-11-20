from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.reports import store

client = TestClient(app)
REPORT_ID = UUID("00000000-0000-0000-0000-000000000001")
REPORT_URL = f"/reports/{REPORT_ID}"
LANDLORD_HEADER = {"X-User-Role": "landlord"}


@pytest.mark.parametrize(
    "body",
    [
        {"status": "in_progress", "planned_fix_note": "Plumber coming Monday"},
        {"status": "resolved"},
        {"planned_fix_note": "Plumber coming Tuesday"},
    ],
)
def test_landlord_can_update_report(monkeypatch, body):
    updated_report = {
        "id": str(REPORT_ID),
        "status": body.get("status", "open"),
        "planned_fix_note": body.get("planned_fix_note", "Existing note"),
        "updated_at": "2026-11-19T15:00:00Z",
    }

    def fake_update_report(report_id, status, planned_fix_note):
        assert report_id == REPORT_ID
        assert status == body.get("status")
        assert planned_fix_note == body.get("planned_fix_note")
        return updated_report

    monkeypatch.setattr(store, "update_report", fake_update_report)
    response = client.patch(REPORT_URL, headers=LANDLORD_HEADER, json=body)

    assert response.status_code == 200
    assert response.json() == updated_report


def unexpected_update(*args):
    pytest.fail("The store should only be called for a valid landlord update")


@pytest.mark.parametrize("headers", [{}, {"X-User-Role": "tenant"}, {"X-User-Role": "admin"}])
def test_only_landlords_can_update_reports(monkeypatch, headers):
    monkeypatch.setattr(store, "update_report", unexpected_update)
    response = client.patch(REPORT_URL, headers=headers, json={"status": "resolved"})

    assert response.status_code == 403


@pytest.mark.parametrize("status", ["open", "seen", "invalid", None])
def test_invalid_update_status_is_rejected(monkeypatch, status):
    monkeypatch.setattr(store, "update_report", unexpected_update)
    response = client.patch(REPORT_URL, headers=LANDLORD_HEADER, json={"status": status})

    assert response.status_code == 422


def test_empty_update_is_rejected(monkeypatch):
    monkeypatch.setattr(store, "update_report", unexpected_update)
    response = client.patch(REPORT_URL, headers=LANDLORD_HEADER, json={})

    assert response.status_code == 422


def test_missing_report_returns_404(monkeypatch):
    def fake_update_report(report_id, status, planned_fix_note):
        assert report_id == REPORT_ID
        return None

    monkeypatch.setattr(store, "update_report", fake_update_report)
    response = client.patch(REPORT_URL, headers=LANDLORD_HEADER, json={"status": "resolved"})

    assert response.status_code == 404

from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.reports import store

client = TestClient(app)

TEST_UNIT_ID = "00000000-0000-0000-0000-000000000000"
TEST_TENANT_ID = "00000000-0000-0000-0000-000000000001"
REPORT_BODY = {
    "title": "Leaking sink",
    "description": "Water under the sink",
    "unit_id": TEST_UNIT_ID,
    "tenant_id": TEST_TENANT_ID,
}


def test_blank_description_is_rejected():
    response = client.post("/reports", json={**REPORT_BODY, "description": "   "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Description is required"


def test_submit_report_passes_required_fields_to_store(monkeypatch):
    def fake_create_report(title, description, unit_id, tenant_id):
        assert title == REPORT_BODY["title"]
        assert description == REPORT_BODY["description"]
        assert unit_id == UUID(TEST_UNIT_ID)
        assert tenant_id == UUID(TEST_TENANT_ID)
        return {**REPORT_BODY, "status": "open"}

    monkeypatch.setattr(store, "create_report", fake_create_report)
    response = client.post("/reports", json=REPORT_BODY)

    assert response.status_code == 200
    assert response.json() == {**REPORT_BODY, "status": "open"}


@pytest.mark.parametrize("field", ["title", "tenant_id"])
def test_submit_report_requires_title_and_tenant_id(field):
    body = REPORT_BODY.copy()
    del body[field]

    response = client.post("/reports", json=body)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", field]


def test_active_reports_requires_valid_unit_id():
    response = client.get("/reports", params={"unit_id": "not-a-uuid"})
    assert response.status_code == 422

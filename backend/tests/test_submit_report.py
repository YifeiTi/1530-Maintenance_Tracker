from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

TEST_UNIT_ID = "00000000-0000-0000-0000-000000000000"


def test_blank_description_is_rejected():
    response = client.post("/reports", json={"description": "   ", "unit_id": TEST_UNIT_ID})
    assert response.status_code == 400
    assert response.json()["detail"] == "Description is required"


def test_active_reports_requires_valid_unit_id():
    response = client.get("/reports", params={"unit_id": "not-a-uuid"})
    assert response.status_code == 422

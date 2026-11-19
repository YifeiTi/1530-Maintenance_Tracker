from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_blank_description_is_rejected():
    response = client.post("/reports", json={"description": "   ", "unit_id": 1})
    assert response.status_code == 400
    assert response.json()["detail"] == "Description is required"

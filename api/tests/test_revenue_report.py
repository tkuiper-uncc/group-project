from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app)


def test_get_revenue_report():
    response = client.get("/reports/revenue?start=2025-08-01&end=2025-08-05")

    assert response.status_code == 200
    data = response.json()
    assert "total_revenue" in data
    assert isinstance(data["total_revenue"], float)
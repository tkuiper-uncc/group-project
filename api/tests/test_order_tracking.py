from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_order_by_id():

    # Act
    response = client.get("/orders/1")

    # Assert
    assert response.status_code in [200, 404]
    data = response.json()
    assert "id" in data
    assert "status" in data
    assert "order_date" in data

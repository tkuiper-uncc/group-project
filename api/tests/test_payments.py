from fastapi.testclient import TestClient
from main import app
from api.dependencies.database import SessionLocal
from api.models.orders import Order, OrderStatus


client = TestClient(app)


def create_test_order(total_price=20.0):
    db=SessionLocal()
    order = Order(
        customer_name = "Test Customer",
        status = OrderStatus.PENDING,
        description = "Test Order",
        total_price = total_price,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    db.close()
    return order.id


def test_successful_payment():
    order_id = create_test_order(total_price=20.0)

    response = client.post(
        "/payments/",
        json={
            "order_id": order_id,
            "amount": 25.0,
            "method": "credit_card"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["order_id"] == order_id


def test_failed_payment():
    order_id = create_test_order(total_price=20.0)

    response = client.post(
        "/payments/",
        json={
            "order_id": order_id,
            "amount": 15.0, # too low
            "method": "credit_card"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "FAILED"
    assert data["order_id"] == order_id


def test_payment_non_existent_order():
    response = client.post(
        "/payments/",
        json={
            "order_id": 999999, # order doesn't exist
            "amount": 20.0,
            "method": "credit_card"
        }
    )

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Order not found"

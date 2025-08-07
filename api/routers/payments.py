from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..models.payment import Payment, PaymentStatus
from ..models.orders import Order, OrderStatus
from ..schemas.payment import PaymentCreate, PaymentResponse
from ..dependencies.database import get_db
from datetime import datetime


router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)


@router.post("/", response_model=PaymentResponse)
def process_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    # Find the order
    order = db.query(Order).filter(Order.id == payment_data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # simulate payment processing
    if payment_data.amount < order.total_price:
        payment_status = PaymentStatus.FAILED
    else:
        payment_status = PaymentStatus.SUCCESS
        order.status = OrderStatus.DELIVERED

    payment = Payment(
        order_id = payment_data.order_id,
        amount = payment_data.amount,
        method = payment_data.method,
        status = payment_status,
        transaction_date=datetime.now(),
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

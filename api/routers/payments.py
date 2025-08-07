from fastapi import APIRouter, HTTPException, Depends, Response, status
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.payment import Payment, PaymentStatus
from ..models.orders import Order, OrderStatus
from ..schemas.payment import PaymentCreate, PaymentResponse
from ..schemas.payment_update import PaymentUpdate
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


@router.get("/", response_model=List[PaymentResponse])
def get_all_payments(db: Session = Depends(get_db)):
    payments = db.query(Payment).all()
    return [PaymentResponse.from_orm(payment) for payment in payments]


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, update_data: PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment


@router.delete("/{payment_id}", response_model=PaymentResponse)
def delete_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return Response(status_code=204)


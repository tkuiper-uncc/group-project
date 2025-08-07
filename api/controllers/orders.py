from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model, order_details as detail_model, sandwiches as sandwich_model
from ..models import promo_codes as promo_model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import uuid


def create(db: Session, request):
    try:
        # Generate tracking number
        tracking_num = str(uuid.uuid4())[:8].upper()

        new_order = model.Order(
            tracking_number=tracking_num,
            customer_id=request.customer_id,
            customer_name=request.customer_name,
            description=request.description,
            order_type=request.order_type
        )

        total_price = 0

        # Add order details & calculate total
        for d in request.order_details:
            sandwich = db.query(sandwich_model.Sandwich).filter(sandwich_model.Sandwich.id == d.sandwich_id).first()
            if not sandwich:
                raise HTTPException(status_code=404, detail=f"Sandwich ID {d.sandwich_id} not found")
            od = detail_model.OrderDetail(
                sandwich_id=d.sandwich_id,
                amount=d.amount
            )
            total_price += float(sandwich.price) * d.amount
            new_order.order_details.append(od)

        # Apply promo code if present
        discount_amount = 0
        if hasattr(request, 'promo_code') and request.promo_code:
            discount_amount = apply_promo_code(db, request.promo_code, total_price)

        new_order.total_price = total_price - discount_amount

        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def apply_promo_code(db: Session, code: str, order_total: float):
    promo = db.query(promo_model.PromoCode).filter(
        promo_model.PromoCode.code == code,
        promo_model.PromoCode.active == True,
        promo_model.PromoCode.expiration_date >= datetime.utcnow()
    ).first()

    if not promo:
        raise HTTPException(status_code=400, detail="Invalid or expired promo code")

    if promo.usage_limit is not None and promo.times_used >= promo.usage_limit:
        raise HTTPException(status_code=400, detail="Promo code usage limit reached")

    discount_amount = order_total * (promo.discount_percent / 100)
    # Optionally increment usage count here or after successful order commit
    promo.times_used += 1
    db.commit()

    return discount_amount

def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

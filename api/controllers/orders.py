from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model, order_details as detail_model, sandwiches as sandwich_model
from sqlalchemy.exc import SQLAlchemyError
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

        new_order.total_price = total_price

        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


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

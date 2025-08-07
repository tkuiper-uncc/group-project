from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import promo_codes as model
from sqlalchemy.exc import SQLAlchemyError
from ..schemas.promo_codes import PromoCodeCreate, PromoCodeUpdate
from datetime import datetime

def create(db: Session, request: PromoCodeCreate):
    # Check if code already exists
    existing = db.query(model.PromoCode).filter(model.PromoCode.code == request.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Promo code already exists")

    new_promo = model.PromoCode(
        code=request.code,
        discount_percent=request.discount_percent,
        expiration_date=request.expiration_date,
        active=request.active,
        usage_limit=request.usage_limit
    )
    try:
        db.add(new_promo)
        db.commit()
        db.refresh(new_promo)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_promo

def read_all(db: Session):
    return db.query(model.PromoCode).all()

def read_one(db: Session, promo_id: int):
    promo = db.query(model.PromoCode).filter(model.PromoCode.id == promo_id).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")
    return promo

def update(db: Session, promo_id: int, request: PromoCodeUpdate):
    promo = db.query(model.PromoCode).filter(model.PromoCode.id == promo_id)
    if not promo.first():
        raise HTTPException(status_code=404, detail="Promo code not found")
    update_data = request.dict(exclude_unset=True)
    promo.update(update_data, synchronize_session=False)
    db.commit()
    return promo.first()

def delete(db: Session, promo_id: int):
    promo = db.query(model.PromoCode).filter(model.PromoCode.id == promo_id)
    if not promo.first():
        raise HTTPException(status_code=404, detail="Promo code not found")
    promo.delete(synchronize_session=False)
    db.commit()
    return

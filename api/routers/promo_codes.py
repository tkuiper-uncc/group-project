from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers import promo_codes as controller
from ..schemas import promo_codes as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Promo Codes"],
    prefix="/promocodes"
)

@router.post("/", response_model=schema.PromoCode)
def create_promo_code(request: schema.PromoCodeCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.PromoCode])
def read_all_promos(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{promo_id}", response_model=schema.PromoCode)
def read_one_promo(promo_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, promo_id=promo_id)

@router.put("/{promo_id}", response_model=schema.PromoCode)
def update_promo(promo_id: int, request: schema.PromoCodeUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, promo_id=promo_id, request=request)

@router.delete("/{promo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promo(promo_id: int, db: Session = Depends(get_db)):
    controller.delete(db=db, promo_id=promo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

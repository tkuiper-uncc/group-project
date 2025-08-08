from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order, operation_id="create_order")
def create_order(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order], operation_id="read_all_orders")
def read_all_orders(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order, operation_id="read_one_order")
def read_one_order(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order, operation_id="update_order")
def update_order(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}", operation_id="delete_order")
def delete_order(item_id: int, db: Session = Depends(get_db)):
    controller.delete(db=db, item_id=item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

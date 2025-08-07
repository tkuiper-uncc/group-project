from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import sandwiches as controller
from ..schemas import sandwiches as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Sandwiches'],
    prefix="/sandwiches"
)


@router.post("/", response_model=schema.Sandwich, status_code=201)
def create_sandwich(request: schema.SandwichCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Sandwich])
def read_all_sandwiches(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{sandwich_id}", response_model=schema.Sandwich)
def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, sandwich_id=sandwich_id)


@router.put("/{sandwich_id}", response_model=schema.Sandwich)
def update_sandwich(sandwich_id: int, request: schema.SandwichUpdate,
           db: Session = Depends(get_db)):
    return controller.update(db=db, sandwich_id=sandwich_id, request=request)


@router.delete("/{sandwich_id}")
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, sandwich_id=sandwich_id)
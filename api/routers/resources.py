from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import resources as controller
from ..schemas import resources as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Resources'],
    prefix="/resources"
)


@router.post("/", response_model=schema.Resource)
def create_resources(request: schema.ResourceCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Resource])
def read_all_resources(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{resource_id}", response_model=schema.Resource)
def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, resource_id=resource_id)


@router.put("/{resource_id}", response_model=schema.Resource)
def update_resource(resource_id: int, request: schema.ResourceUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, resource_id=resource_id, request=request)


@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, resource_id=resource_id)
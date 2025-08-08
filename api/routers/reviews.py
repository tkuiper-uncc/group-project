from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas import reviews as schema
from ..controllers import reviews as controller

router = APIRouter(
    tags=["Reviews"],
    prefix="/reviews"
)


@router.post("/", response_model=schema.Review, status_code=201)
def create_review(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

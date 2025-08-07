from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.reviews import Review
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_review = Review(
        sandwich_id=request.sandwich_id,
        rating=request.rating,
        comment=request.comment
    )
    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e.__dict__['orig']))
    return new_review

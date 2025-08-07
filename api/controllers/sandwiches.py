from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import sandwiches as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    # Create new sandwich
    new_sandwich = model.Sandwich(
        sandwich_name=request.sandwich_name,
        price=request.price
    )

    try:
        db.add(new_sandwich)
        db.commit()
        db.refresh(new_sandwich)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        if "duplicate key" in error.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sandwich name must be unique"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    return new_sandwich

def read_all(db: Session):
    try:
        sandwiches = db.query(model.Sandwich).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return sandwiches

def read_one(db: Session, sandwich_id: int):
    try:
        sandwich = db.query(model.Sandwich).filter(
            model.Sandwich.id == sandwich_id
        ).first()
        if not sandwich:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sandwich not found"
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return sandwich

def update(db: Session, sandwich_id: int, request):
    try:
        sandwich = db.query(model.Sandwich).filter(
            model.Sandwich.id == sandwich_id
        )
        if not sandwich.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sandwich not found"
            )
        
        update_data = request.dict(exclude_unset=True)
        sandwich.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return sandwich.first()

def delete(db: Session, sandwich_id: int):
    try:
        sandwich = db.query(model.Sandwich).filter(
            model.Sandwich.id == sandwich_id
        )
        if not sandwich.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sandwich not found"
            )
        
        sandwich.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        if "foreign key constraint" in error.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete: sandwich is referenced in recipes or orders"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from sqlalchemy import func
from ..models.reviews import Review
from ..models.sandwiches import Sandwich

def get_popular_sandwiches(db: Session):
    results = db.query(
        Sandwich.id,
        Sandwich.sandwich_name,
        func.count(Review.id).label("review_count"),
        func.avg(Review.rating).label("avg_rating")
    ).join(Review).group_by(Sandwich.id).order_by(func.avg(Review.rating).desc()).all()

    return [
        {
            "id": row.id,
            "sandwich_name": row.sandwich_name,
            "review_count": row.review_count,
            "avg_rating": round(row.avg_rating, 2)
        }
        for row in results
    ]

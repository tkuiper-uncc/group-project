from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..controllers import sandwiches as controller
from ..schemas import sandwiches as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Sandwiches'],
    prefix="/sandwiches"
)


@router.get("/popular", operation_id="sandwiches_get_popular")
def get_popular(db: Session = Depends(get_db)):
    return controller.get_popular_sandwiches(db)


@router.get("/featured")
def get_featured_sandwiches():
    """Simple featured endpoint that returns static data"""
    return {
        "featured": [
            {"id": 1, "name": "Classic BLT", "description": "Our most popular sandwich"},
            {"id": 2, "name": "Veggie Delight", "description": "A vegetarian favorite"},
            {"id": 3, "name": "Spicy Chicken", "description": "For those who like heat"},
        ]
    }


@router.get("/least-popular")
def get_least_popular_sandwiches(
    days: int = Query(30, ge=1, le=365, description="Lookback window in days"),
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return controller.get_least_popular_sandwiches(db=db, days=days, limit=limit)


@router.get("/most-complaints")
def get_sandwiches_with_most_complaints(
    days: int = Query(90, ge=1, le=365),
    rating_threshold: int = Query(3, ge=1, le=5, description="Ratings < threshold count as complaints"),
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return controller.get_sandwiches_with_most_complaints(
        db=db, days=days, rating_threshold=rating_threshold, limit=limit
    )


@router.get("/insights")
def sandwiches_insights(
    days_popularity: int = Query(30, ge=1, le=365),
    days_complaints: int = Query(90, ge=1, le=365),
    rating_threshold: int = Query(3, ge=1, le=5),
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return controller.get_sandwiches_insights(
        db=db,
        days_popularity=days_popularity,
        days_complaints=days_complaints,
        rating_threshold=rating_threshold,
        limit=limit,
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


@router.get("/popular")
def get_popular(db: Session = Depends(get_db)):
    return controller.get_popular_sandwiches(db)

@router.get("/featured")
def get_featured_sandwiches():
    """Simple featured endpoint that returns static data"""
    return {
        "featured": [
            {"id": 1, "name": "Classic BLT", "description": "Our most popular sandwich"},
            {"id": 2, "name": "Veggie Delight", "description": "A vegetarian favorite"},
            {"id": 3, "name": "Spicy Chicken", "description": "For those who like heat"}
        ]
    }

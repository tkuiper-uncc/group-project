from typing import ItemsView

from sqlalchemy import func
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..dependencies.database import get_db
from ..models.orders import Order

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)


@router.get("/revenue")
def get_revenue_report(start: str, end: str, db: Session = Depends(get_db)):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format.  Use YYYY-MM-DD")

    revenue = db.query(func.sum(Order.total_price))\
            .filter(Order.order_date >= start_date)\
            .filter(Order.order_date <= end_date)\
            .scalar()

    return {
        "start_date": start,
        "end_date": end,
        "total_revenue": revenue or 0.0}
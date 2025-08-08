from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    method: str


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    method: str
    status: PaymentStatus
    transaction_date: datetime

    class Config:
        from_attributes = True

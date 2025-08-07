from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail
from enum import Enum


class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None


class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(OrderBase):
    id: int
    status: OrderStatus
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None
    total_price: Optional[float] = None

    class ConfigDict:
        from_attributes = True

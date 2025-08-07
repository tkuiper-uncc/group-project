from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetailCreate, OrderDetail
from enum import Enum



class OrderType(str, Enum):
    TAKEOUT = "takeout"
    DELIVERY = "delivery"
    PICKUP = "pickup"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None
    order_type: Optional[OrderType] = OrderType.TAKEOUT

class OrderCreate(OrderBase):
    customer_id: Optional[int] = None  # Registered user
    order_details: List[OrderDetailCreate]  # Must include details


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[OrderStatus] = None
    order_type: Optional[OrderType] = None


class Order(OrderBase):
    id: int
    tracking_number: str
    status: OrderStatus
    order_date: datetime
    total_price: float
    order_details: List[OrderDetail]

    class ConfigDict:
        from_attributes = True
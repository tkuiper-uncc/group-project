from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DECIMAL, Enum, DateTime, func, Float, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
import enum
from .customers import Customer
import uuid


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderType(str, enum.Enum):
    TAKEOUT = "takeout"
    DELIVERY = "delivery"
    PICKUP = "pickup"


class OrderType(str, enum.Enum):
    TAKEOUT = "takeout"
    DELIVERY = "delivery"
    PICKUP = "pickup"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    tracking_number = Column(String(20), unique=True, index=True, nullable=False, default=uuid.uuid4)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    customer_name = Column(String(100), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    order_type = Column(Enum(OrderType), nullable=False, default=OrderType.TAKEOUT)
    order_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    description = Column(String(300))
    total_price = Column(DECIMAL(10, 2))

    order_details = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order")
    customer = relationship("Customer", back_populates="orders")

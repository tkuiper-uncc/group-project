from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Enum, Float, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
import enum


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    total_price = Column(Float)

    order_details = relationship("OrderDetail", back_populates="order")
    payments = relationship("Payment", back_populates="order")

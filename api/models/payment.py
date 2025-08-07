from sqlalchemy import Column, Integer, String, Float, ForeignKey, DATETIME, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
from enum import Enum as PyEnum


class PaymentStatus(PyEnum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String(50))
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_date = Column(DATETIME, default=datetime.now)

    order = relationship("Order", back_populates="payments")



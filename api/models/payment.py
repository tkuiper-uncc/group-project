from sqlalchemy import Column, Integer, String, Float, ForeignKey, DATETIME, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
import enum


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String(50))
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_date = Column(DATETIME, default=datetime.now)

    order = relationship("Order", backref="payments")

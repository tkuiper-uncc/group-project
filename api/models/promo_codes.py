from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from datetime import datetime
from ..dependencies.database import Base

class PromoCode(Base):
    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    discount_percent = Column(Float, nullable=False)  # e.g., 20.0 for 20%
    expiration_date = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    usage_limit = Column(Integer, nullable=True)  # optional limit on how many times it can be used
    times_used = Column(Integer, default=0, nullable=False)

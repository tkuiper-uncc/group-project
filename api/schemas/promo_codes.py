from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PromoCodeBase(BaseModel):
    code: str
    discount_percent: float
    expiration_date: datetime
    active: Optional[bool] = True
    usage_limit: Optional[int] = None

class PromoCodeCreate(PromoCodeBase):
    pass

class PromoCodeUpdate(BaseModel):
    discount_percent: Optional[float] = None
    expiration_date: Optional[datetime] = None
    active: Optional[bool] = None
    usage_limit: Optional[int] = None

class PromoCode(PromoCodeBase):
    id: int
    times_used: int

    class Config:
        orm_mode = True

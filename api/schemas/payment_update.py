from typing import Optional
from pydantic import BaseModel


class PaymentUpdate(BaseModel):
    amount: Optional[float]
    method: Optional[str]
    status: Optional[str]
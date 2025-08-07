from pydantic import BaseModel, Field
from typing import Optional

class ReviewCreate(BaseModel):
    sandwich_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class Review(BaseModel):
    id: int
    sandwich_id: int
    rating: int
    comment: Optional[str]

    class ConfigDict:
        from_attributes = True

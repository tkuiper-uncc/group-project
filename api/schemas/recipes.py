from pydantic import BaseModel
from typing import List, Optional
from .resources import Resource

class RecipeResourceBase(BaseModel):
    resource_id: int
    amount: int

class RecipeResource(RecipeResourceBase):
    resource: Resource


class RecipeBase(BaseModel):
    sandwich_id: int
    is_vegetarian: bool

class RecipeCreate(RecipeBase):
    resources: List[RecipeResourceBase]

class RecipeUpdate(BaseModel):
    sandwich_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    resources: List[RecipeResource]

    class ConfigDict:
        from_attributes = True
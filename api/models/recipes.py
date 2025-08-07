from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

recipe_resource = Table(
    'recipe_resources',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('resource_id', Integer, ForeignKey('resources.id'), primary_key=True),
    Column('amount', Integer, nullable=False)
)

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    is_vegetarian = Column(Boolean, default=False, nullable=False)

    sandwich = relationship("Sandwich", back_populates="recipes")
    resources = relationship("Resource", secondary=recipe_resource, back_populates="recipes")
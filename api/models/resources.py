from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(512), nullable=False)
    type = Column(String(512), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    unit = Column(String(128), nullable=False)

    recipes = relationship(
        "MenuItemRecipe", secondary="menu_items_recipes_resources", back_populates="resources"
    )

    used_in_recipes = relationship("RecipeIngredient", back_populates="resource")

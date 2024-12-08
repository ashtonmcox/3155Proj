from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
from .recipes import MenuItemRecipe
from .resources import Resource


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    quantity = Column(Float, nullable=False)

    recipe = relationship("MenuItemRecipe", back_populates="ingredients")  
    resource = relationship("Resource", back_populates="used_in_recipes")


from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime, Date, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class MenuItemRecipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(512), nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String(512))
    recipes_id = Column(Integer, nullable=False, unique=True)
    recipes_menu_item_id = Column(Integer, nullable=False)
    recipes_name = Column(String(512), nullable=False)
    recipes_description = Column(String(512))
    recipes_resource = Column(String(512), nullable=False)
    recipes_instructions = Column(String(512), nullable=False)
    recipes_preparation_time = Column(Integer)
    recipes_servings = Column(Integer)
    recipes_created_at = Column(DateTime, default=datetime.utcnow)
    calories = Column(Integer)

    resources = relationship(
        "Resource", secondary="menu_items_recipes_resources", back_populates="recipes"
    )
    order_details = relationship(
        "OrderDetailOrderMenuItemRecipe", back_populates="recipes"
    )
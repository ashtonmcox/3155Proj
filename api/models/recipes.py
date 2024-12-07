from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class MenuItemRecipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(512), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(512), nullable=True)
    dietary_category = Column(String(512), nullable=True)
    description = Column(String(512), nullable=True)
    resource = Column(String(512), nullable=False)
    instructions = Column(String(512), nullable=False)
    preparation_time = Column(String(512), nullable=True)
    servings = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    calories = Column(Integer, nullable=True)

    
    resources = relationship(
        "Resource", secondary="menu_items_recipes_resources", back_populates="recipes"
    )

    order_details = relationship(
        "OrderDetail", back_populates="recipes"
    )

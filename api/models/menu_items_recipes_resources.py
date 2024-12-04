from sqlalchemy import Table, Column, Integer, ForeignKey
from ..dependencies.database import Base


menu_items_recipes_resources = Table(
    "menu_items_recipes_resources", 
    Base.metadata,
    Column("menu_item_recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("resources.id"), primary_key=True)
)
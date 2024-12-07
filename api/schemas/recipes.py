from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class MenuItemRecipeBase(BaseModel):
    name: str
    price: float
    category: str
    dietary_category: str
    description: str
    resource: str
    instructions: str
    preparation_time: str
    servings: int
    calories: int


class MenuItemRecipeCreate(MenuItemRecipeBase):
    pass  


class MenuItemRecipeUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    dietary_category: Optional[str] = None
    description: Optional[str] = None
    resource: Optional[str] = None
    instructions: Optional[str] = None
    preparation_time: Optional[str] = None
    servings: Optional[int] = None
    calories: Optional[int] = None


class MenuItemRecipe(MenuItemRecipeBase):
    id: int
    resources: List[int] = []  

    class Config:
        from_attributes = True 

from typing import Optional
from pydantic import BaseModel


class RecipeIngredientBase(BaseModel):
    recipe_id: int
    resource_id: int
    quantity: float


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredientUpdate(BaseModel):
    recipe_id: Optional[int] = None
    resource_id: Optional[int] = None
    quantity: Optional[float] = None


class RecipeIngredient(RecipeIngredientBase):
    id: int

    class Config:
        from_attributes = True

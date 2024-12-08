from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..controllers import recipe_ingredients as controller
from ..schemas import recipe_ingredients as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Recipe Ingredients"],
    prefix="/recipeingredients"
)


@router.post("/", response_model=schema.RecipeIngredient)
def create(request: schema.RecipeIngredientCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.RecipeIngredient])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{recipe_ingredient_id}", response_model=schema.RecipeIngredient)
def read_one(recipe_ingredient_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, recipe_ingredient_id=recipe_ingredient_id)


@router.put("/{recipe_ingredient_id}", response_model=schema.RecipeIngredient)
def update(recipe_ingredient_id: int, request: schema.RecipeIngredientUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, recipe_ingredient_id=recipe_ingredient_id, update_data=request.dict(exclude_unset=True))


@router.delete("/{recipe_ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(recipe_ingredient_id: int, db: Session = Depends(get_db)):
    controller.delete(db=db, recipe_ingredient_id=recipe_ingredient_id)
    return {"detail": "Recipe ingredient deleted successfully"}

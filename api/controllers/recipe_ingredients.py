from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import recipe_ingredients as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.RecipeIngredient(
        recipe_id=request.recipe_id,
        resource_id=request.resource_id,
        quantity=request.quantity
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.RecipeIngredient).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, recipe_ingredient_id: int):
    try:
        recipe_ingredient = (
            db.query(model.RecipeIngredient)
            .filter(model.RecipeIngredient.id == recipe_ingredient_id)
            .first()
        )
        if not recipe_ingredient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe ingredient not found!",
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return recipe_ingredient


def update(db: Session, recipe_ingredient_id: int, update_data: dict):
    try:
        recipe_ingredient = (
            db.query(model.RecipeIngredient)
            .filter(model.RecipeIngredient.id == recipe_ingredient_id)
            .first()
        )
        if not recipe_ingredient:
            raise HTTPException(status_code=404, detail="Recipe ingredient not found")

        for key, value in update_data.items():
            setattr(recipe_ingredient, key, value)

        db.commit()
        db.refresh(recipe_ingredient)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=400, detail=error)
    return recipe_ingredient


def delete(db: Session, recipe_ingredient_id: int):
    recipe_ingredient = (
        db.query(model.RecipeIngredient)
        .filter(model.RecipeIngredient.id == recipe_ingredient_id)
        .first()
    )
    if not recipe_ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe ingredient not found",
        )
    db.delete(recipe_ingredient)
    db.commit()
    return True

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import recipes as model
from ..schemas.recipes import MenuItemRecipeCreate, MenuItemRecipeUpdate

def create(db: Session, request: MenuItemRecipeCreate):
    new_menu_item = model.MenuItemRecipe(
        name=request.name,
        price=request.price,
        category=request.category,
        dietary_category=request.dietary_category,
        description=request.description,
        instructions=request.instructions,
        preparation_time=request.preparation_time,
        servings=request.servings,
        calories=request.calories,
    )

    try:
        db.add(new_menu_item)
        db.commit()
        db.refresh(new_menu_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_menu_item

def read_all(db: Session):
    try:
        result = db.query(model.MenuItemRecipe).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_by_dietary_category(db: Session, dietary_category: str):
    try:
        query = db.query(model.MenuItemRecipe)
        
        if dietary_category:
            query = query.filter(
                model.MenuItemRecipe.dietary_category.ilike(f"%{dietary_category}%")
            )
        
        result = query.all()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No menu items found for dietary category: {dietary_category}",
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

def read_one(db: Session, item_id: int):
    try:
        menu_item = db.query(model.MenuItemRecipe).filter(model.MenuItemRecipe.id == item_id).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return menu_item

def update(db: Session, item_id: int, request):
    try:
        menu_item_query = db.query(model.MenuItemRecipe).filter(model.MenuItemRecipe.id == item_id)
        
        menu_item = menu_item_query.first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")
        
        update_data = request.dict(exclude_unset=True)
        
        menu_item_query.update(update_data, synchronize_session=False)
        
        db.commit()
        
        db.refresh(menu_item)
        
        return menu_item
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)





def delete(db: Session, item_id: int):
    try:
        menu_item = db.query(model.MenuItemRecipe).filter(model.MenuItemRecipe.id == item_id)
        if not menu_item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")
        menu_item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

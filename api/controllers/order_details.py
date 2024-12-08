from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import order_details as model, recipes as recipe_model, orders as order_model, recipe_ingredients as ri_model, resources as resource_model
from ..models.orders import Order
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    # Fetch the menu item (recipe) being ordered
    menu_item = db.query(recipe_model.MenuItemRecipe).filter(
        recipe_model.MenuItemRecipe.id == request.menu_item_id).first()

    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")

    # Fetch the recipe ingredients for the menu item
    recipe_ingredients = db.query(ri_model.RecipeIngredient).filter(
        ri_model.RecipeIngredient.recipe_id == menu_item.id).all()

    # Check if there are enough resources for each ingredient
    for ingredient in recipe_ingredients:
        resource = db.query(resource_model.Resource).filter(
            resource_model.Resource.id == ingredient.resource_id).first()

        if not resource:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Resource {ingredient.resource_id} not found.")

        required_quantity = ingredient.quantity * request.quantity  # Quantity needed for the ordered amount

        if resource.amount < required_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough {resource.name}. Available: {resource.amount} {resource.unit}, "
                       f"Required: {required_quantity} {resource.unit}."
            )

    # Create the new order detail
    new_item = model.OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        quantity=request.quantity
    )

    # Get the price of the menu item
    menu_item_price = menu_item.price

    # Calculate the total price for the ordered quantity
    total_item_price = menu_item_price * request.quantity

    try:
        # Add the new order detail to the database
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        # Update the total price of the order
        order = db.query(order_model.Order).filter(order_model.Order.id == request.order_id).first()
        if order:
            order.total_price += total_item_price
            db.commit()
            db.refresh(order)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item
def read_all(db: Session):
    try:
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, order_detail_id: int):
    try:
        order_detail = db.query(model.OrderDetail).filter(model.OrderDetail.id == order_detail_id).first()
        if not  order_detail:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order detail not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return  order_detail

def update(db: Session, order_detail_id: int, update_data: dict):
    try:
        order_detail = db.query(model.OrderDetail).filter(model.OrderDetail.id == order_detail_id).first()
        if not order_detail:
            raise HTTPException(status_code=404, detail="OrderDetail not found")

        for key, value in update_data.items():
            setattr(order_detail, key, value)

        db.commit()
        db.refresh(order_detail)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=400, detail=error)
    return order_detail

def get(db: Session, order_detail_id: int):
    order_detail = db.query(model.OrderDetail).filter(model.OrderDetail.id == order_detail_id).first()
    if not order_detail:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return order_detail


def delete(db: Session, order_detail_id: int):
    try:
        # Fetch the order detail to be deleted
        order_detail = db.query(model.OrderDetail).filter(model.OrderDetail.id == order_detail_id).first()
        if not order_detail:
            raise HTTPException(status_code=404, detail="Order detail not found")

        # Fetch the associated menu item and its price
        menu_item = db.query(recipe_model.MenuItemRecipe).filter(
            recipe_model.MenuItemRecipe.id == order_detail.menu_item_id).first()

        if not menu_item:
            raise HTTPException(status_code=404, detail="Menu item not found for this order detail")

        # Calculate the price to subtract from the order total
        total_item_price = menu_item.price * order_detail.quantity

        # Fetch the associated order
        order = db.query(order_model.Order).filter(order_model.Order.id == order_detail.order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Associated order not found")

        # Subtract the item's total price from the order's total price
        order.total_price -= total_item_price

        # Delete the order detail
        db.delete(order_detail)
        db.commit()

        # Update the order after the deletion
        db.refresh(order)

        return {"message": "Order detail deleted successfully and order total updated"}

    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', 'An error occurred'))
        raise HTTPException(status_code=400, detail=error)
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.order_details import OrderDetail
from ..models.recipes import MenuItemRecipe as MenuItem
from fastapi import HTTPException


def get_menu_item_popularity(db: Session):
    try:
        # Perform a query to count how many times each menu item appears in order details
        result = db.query(
            OrderDetail.menu_item_id,
            func.count(OrderDetail.menu_item_id).label("popularity_count")
        ).group_by(OrderDetail.menu_item_id).all()

        # Fetch the menu item details along with the popularity count
        menu_item_popularity = []
        for menu_item_id, count in result:
            menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
            if not menu_item:
                raise HTTPException(status_code=404, detail=f"Menu item with ID {menu_item_id} not found.")
            menu_item_popularity.append({
                "menu_item_id": menu_item.id,
                "name": menu_item.name,
                "popularity_count": count
            })

        return menu_item_popularity
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving menu item popularity.")

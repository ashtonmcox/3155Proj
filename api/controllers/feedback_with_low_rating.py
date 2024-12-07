from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import feedback as model
from ..models.order_details import OrderDetail
from ..models.recipes import MenuItemRecipe as MenuItem
from fastapi import HTTPException


def get_feedback_with_low_rating(db: Session):
    try:
        # Query feedback with score <= 3
        low_rated_feedback = db.query(model.Feedback).filter(model.Feedback.score <= 3).all()

        feedback_details = []

        for feedback in low_rated_feedback:
            # Get the order details for the order ID
            order_details = db.query(OrderDetail).filter(OrderDetail.order_id == feedback.order_id).all()

            menu_items = []
            for order_detail in order_details:
                menu_item = db.query(MenuItem).filter(MenuItem.id == order_detail.menu_item_id).first()
                if menu_item:
                    menu_items.append({
                        "menu_item_id": menu_item.id,
                        "name": menu_item.name
                    })

            feedback_details.append({
                "order_id": feedback.order_id,
                "menu_items": menu_items,
                "rating": feedback.score,
                "content": feedback.content
            })

        return feedback_details

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving feedback with low ratings.")

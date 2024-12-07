from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import feedback_with_low_rating as controller
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Feedback with Low Ratings"],
    prefix="/low-rating-feedback"
)

@router.get("/", response_model=list[dict])
def get_low_rating_feedback(db: Session = Depends(get_db)):
    """
    Get all feedback with a rating of 3 or less, including the order number, menu items, rating, and content.
    """
    return controller.get_feedback_with_low_rating(db=db)

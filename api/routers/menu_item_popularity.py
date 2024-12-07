from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import menu_item_popularity as controller
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Menu Item Popularity"],
    prefix="/menu-item-popularity"
)

@router.get("/", response_model=list[dict])
def get_popularity(db: Session = Depends(get_db)):\
    return controller.get_menu_item_popularity(db=db)

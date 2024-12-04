from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import feedback as controller
from ..schemas import feedback as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Feedback'],
    prefix="/feedback"
)

@router.post("/", response_model=schema.Feedback)
def create(request: schema.FeedbackCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Feedback])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.Feedback)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.Feedback)
def update(item_id: int, request: schema.FeedbackUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

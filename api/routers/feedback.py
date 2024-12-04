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

@router.get("/{feedback_id}", response_model=schema.Feedback)
def read_one(feedback_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, feedback_id=feedback_id)

@router.put("/{feedback_id}", response_model=schema.Feedback)
def update(feedback_id: int, request: schema.FeedbackUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, feedback_id=feedback_id)

@router.delete("/{feedback_id}")
def delete(feedback_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, feedback_id=feedback_id)

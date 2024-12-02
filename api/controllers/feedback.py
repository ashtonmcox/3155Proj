from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import feedback as model


def create(db: Session, request):
    new_feedback = model.Feedback(
        user_id=request.user_id,
        content=request.content,
        order_details_orders_id=request.order_details_orders_id,
        score=request.score,
    )

    try:
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_feedback


def read_all(db: Session):
    try:
        result = db.query(model.Feedback).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, feedback_id: int):
    try:
        feedback = db.query(model.Feedback).filter(model.Feedback.id == feedback_id).first()
        if not feedback:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return feedback


def update(db: Session, feedback_id: int, request):
    try:
        feedback = db.query(model.Feedback).filter(model.Feedback.id == feedback_id)
        if not feedback.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found!")
        update_data = request.dict(exclude_unset=True)
        feedback.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return feedback.first()


def delete(db: Session, feedback_id: int):
    try:
        feedback = db.query(model.Feedback).filter(model.Feedback.id == feedback_id)
        if not feedback.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found!")
        feedback.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

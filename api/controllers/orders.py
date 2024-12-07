from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from ..models import orders as model
from datetime import date


def create(db: Session, request):
    new_order = model.Order(
        user_id=request.user_id,
        status=request.status,
        tracking_number=request.tracking_number,
        order_type=request.order_type,
        total_price=request.total_price,
        date=request.date
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, order_id: int):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


def update(db: Session, order_id: int, request):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
        update_data = request.dict(exclude_unset=True)
        order.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order.first()


def delete(db: Session, order_id: int):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
        order.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def read_one_by_tracking_number(db: Session, tracking_number: str):
    
    order = db.query(model.Order).filter(model.Order.tracking_number == tracking_number).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order
def read_by_date_range(db: Session, start_date: date, end_date: date):
    try:
        orders = db.query(model.Order).filter(
            model.Order.date >= start_date,
            model.Order.date <= end_date
        ).all()
        if not orders:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found within the specified date range.")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", "An error occurred"))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return orders


def get_revenue_by_date(db: Session, target_date: date):
    try:
        total_revenue = db.query(func.sum(model.Order.total_price)) \
            .filter(func.date(model.Order.date) == target_date).scalar()

        if total_revenue is None:
            raise HTTPException(status_code=404, detail="No orders found for this date")

        total_revenue = round(total_revenue, 2)

        return {"total_revenue": total_revenue}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
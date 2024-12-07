from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db
from datetime import date
from pydantic import BaseModel


router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{tracking_number}", response_model=schema.Order)
def read_one_by_tracking_number(tracking_number: str, db: Session = Depends(get_db)):
    return controller.read_one_by_tracking_number(db, tracking_number=tracking_number)

@router.get("/{order_id}", response_model=schema.Order)
def read_one(order_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, order_id=order_id)


@router.put("/{order_id}", response_model=schema.Order)
def update(order_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, order_id=order_id)


@router.delete("/{order_id}")
def delete(order_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, order_id=order_id)

class DateRange(BaseModel):
    start_date: date
    end_date: date

@router.post("/date-range", response_model=list[schema.Order])
def read_by_date_range(date_range: DateRange, db: Session = Depends(get_db)):
    return controller.read_by_date_range(db=db, start_date=date_range.start_date, end_date=date_range.end_date)

from pydantic import BaseModel
from datetime import date

class DateInput(BaseModel):
    date: date

@router.post("/revenue", response_model=dict)
def get_revenue(request: DateInput, db: Session = Depends(get_db)):
    return controller.get_revenue_by_date(db=db, target_date=request.date)


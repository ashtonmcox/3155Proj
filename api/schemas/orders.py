from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel




class OrderBase(BaseModel):
   user_id: int
   status: str
   tracking_number: str
   total_price: float
   date: datetime 




class OrderCreate(OrderBase):
   total_price: float 


class OrderUpdate(BaseModel):
   user_id: Optional[int] = None
   status: Optional[str] = None
   tracking_number: Optional[str] = None
   total_price: Optional[float] = None
   date: Optional[datetime] = None




class Order(OrderBase):
   id: int
   details: List[int] = [] 
   class Config:
       from_attributes = True 
from typing import Optional
from pydantic import BaseModel


class FeedbackBase(BaseModel):
    user_id: int
    content: str
    order_details_orders_id: int
    score: int  


class FeedbackCreate(FeedbackBase):
    pass  


class FeedbackUpdate(BaseModel):
    user_id: Optional[int] = None
    content: Optional[str] = None
    order_details_orders_id: Optional[int] = None
    score: Optional[int] = None


class Feedback(FeedbackBase):
    id: int

    class Config:
        from_attributes = True  

from typing import Optional
from pydantic import BaseModel
from datetime import date


class PromotionBase(BaseModel):
    code: str
    description: Optional[str] = None
    expiration_date: date
    discount_value: Optional[float] = None  
    discount_percentage: Optional[float] = None  


class PromotionCreate(PromotionBase):
    pass  


class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    expiration_date: Optional[date] = None
    discount_value: Optional[float] = None
    discount_percentage: Optional[float] = None


class Promotion(PromotionBase):
    id: int

    class Config:
        from_attributes = True  

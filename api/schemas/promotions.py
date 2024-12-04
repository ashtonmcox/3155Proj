from typing import Optional
from pydantic import BaseModel
from datetime import date


class PromotionBase(BaseModel):
    promotion_code: str
    description: Optional[str] = None
    expiration_date: date
    discount_percent: Optional[float] = None  


class PromotionCreate(PromotionBase):
    pass  


class PromotionUpdate(BaseModel):
    promotion_code: Optional[str] = None
    description: Optional[str] = None
    expiration_date: Optional[date] = None
    discount_percent: Optional[float] = None


class Promotion(PromotionBase):
    id: int

    class Config:
        from_attributes = True  

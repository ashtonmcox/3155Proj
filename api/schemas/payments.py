from typing import Optional
from pydantic import BaseModel


class PaymentBase(BaseModel):
    order_id: int
    card_information: str
    transaction_status: str
    payment_type: str
    promotion_code: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass  


class PaymentUpdate(BaseModel):
    order_id: Optional[int] = None
    card_information: Optional[str] = None
    transaction_status: Optional[str] = None
    payment_type: Optional[str] = None
    promotion_code: Optional[str] = None


class Payment(PaymentBase):
    id: int

    class Config:
        from_attributes = True  

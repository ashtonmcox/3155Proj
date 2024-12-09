from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: str
    phone_number: str
    address: str


class UserCreate(UserBase):
    pass  


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None


class User(UserBase):
    id: int
    orders: Optional[list] = []  

    class Config:
        from_attributes = True
        orm_mode = True

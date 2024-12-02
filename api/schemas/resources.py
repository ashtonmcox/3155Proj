from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ResourceBase(BaseModel):
    name: str  
    amount: float  
    type: str  
    unit: str  


class ResourceCreate(ResourceBase):
    pass  


class ResourceUpdate(BaseModel):
    name: Optional[str] = None  
    amount: Optional[float] = None  
    type: Optional[str] = None  
    unit: Optional[str] = None  


class Resource(ResourceBase):
    id: int  

    class Config:
        from_attributes = True  

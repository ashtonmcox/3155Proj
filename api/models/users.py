from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime, Date, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(512), nullable=False)
    email = Column(String(512), nullable=False, unique=True)
    phone_number = Column(String(20))
    address = Column(String(512))

    orders = relationship("OrderDetailOrder", back_populates="user")
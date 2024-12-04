from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base




class Order(Base):
   __tablename__ = "orders"


   id = Column(Integer, primary_key=True, index=True, autoincrement=True)
   user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  
   status = Column(String(512), nullable=False)
   date = Column(DateTime, default=datetime.utcnow)
   tracking_number = Column(Integer, nullable=False)
   order_type = Column(String(10), nullable=False)
   total_price = Column(Float, nullable=False)


   users = relationship("User", back_populates="orders")
   order_details = relationship("OrderDetail", back_populates="orders")
   feedback = relationship("Feedback", back_populates="orders")

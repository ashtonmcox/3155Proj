from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(512), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    tracking_number = Column(String(128))
    total_price = Column(DECIMAL(10, 2))

    user = relationship("User", back_populates="orders")
    details = relationship("OrderDetail", back_populates="order")
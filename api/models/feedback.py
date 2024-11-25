from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime, Date, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String(512), nullable=False)
    order_details_orders_id = Column(Integer, ForeignKey("order.id"))
    score = Column(Integer, CheckConstraint("score BETWEEN 1 AND 5"))

    user = relationship("User")
    order = relationship("Order")
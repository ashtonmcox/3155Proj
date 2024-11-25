from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime, date
from ..dependencies.database import Base



class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(128), nullable=False, unique=True)
    description = Column(String(512))
    expiration_date = Column(date, nullable=False)
    discount_value = Column(DECIMAL(10, 2))
    discount_percentage = Column(DECIMAL(5, 2))
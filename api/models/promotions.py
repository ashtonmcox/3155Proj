from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Date, Float
from sqlalchemy.orm import relationship
from datetime import datetime, date
from ..dependencies.database import Base



class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promotion_code = Column(String(128), nullable=False, unique=True)
    description = Column(String(512))
    expiration_date = Column(Date, nullable=False)
    discount_percent = Column(Float)

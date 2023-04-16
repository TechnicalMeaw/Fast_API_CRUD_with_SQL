from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False, default=0)
    is_sale = Column(Boolean, default= False)
    created_at = Column(DateTime, default= datetime.datetime.now)
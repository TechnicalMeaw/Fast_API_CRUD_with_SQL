from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, TextClause
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False, server_default=TextClause("0"))
    is_sale = Column(Boolean, server_default=TextClause("False"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=TextClause("Now()"))
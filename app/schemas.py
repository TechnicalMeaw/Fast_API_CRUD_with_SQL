from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    name : str
    price: int
    inventory: int
    is_sale: bool = True


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id : int
    created_at : datetime

    class Config:
        orm_mode = True

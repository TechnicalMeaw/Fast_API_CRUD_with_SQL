from pydantic import BaseModel, EmailStr
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



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

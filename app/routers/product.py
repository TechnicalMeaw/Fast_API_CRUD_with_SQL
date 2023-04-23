from fastapi import status, Response, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/items",
    tags= ["Products"]
)

@router.get("/", response_model=List[schemas.Product])
def test_posts(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Product)
def add_item(item : schemas.ProductCreate, db: Session = Depends(get_db)):
    new_item = models.Product(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item



@router.get("/{id}", response_model= schemas.Product)
def get_item(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    
    return product
    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    
    product.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/items/{id}", response_model= schemas.Product)
def update_item(id: int, item:schemas.ProductCreate, db: Session = Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.id == id)

    if not product_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    
    product_query.update(item.dict(), synchronize_session=False)
    db.commit()
    return product_query.first()

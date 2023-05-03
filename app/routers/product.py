from fastapi import status, Response, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/items",
    tags= ["Products"]
)

@router.get("/", response_model=List[schemas.ProductOut])
def test_posts(db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user), 
               limit : int = 10, skip: int = 0, search: Optional[str] = ""):
    # products = db.query(models.Product).filter(models.Product.name.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Product, func.count(models.Vote.product_id).label("votes")).join(models.Vote, models.Product.id == models.Vote.product_id, isouter=True).group_by(models.Product.id).all()
    return results


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Product)
def add_item(item : schemas.ProductCreate, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    new_item = models.Product(owner_id = current_user.id, **item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item



@router.get("/{id}", response_model= schemas.ProductOut)
def get_item(id: int, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    # product = db.query(models.Product).filter(models.Product.id == id).first()
    product = db.query(models.Product, func.count(models.Vote.product_id).label("votes")).join(models.Vote, models.Product.id == models.Vote.product_id, isouter=True).group_by(models.Product.id).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    
    return product
    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    product_query = db.query(models.Product).filter(models.Product.id == id)

    product = product_query.first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    product_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model= schemas.Product)
def update_item(id: int, item:schemas.ProductCreate, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    product_query = db.query(models.Product).filter(models.Product.id == id)

    product = product_query.first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    product_query.update(item.dict(), synchronize_session=False)
    db.commit()
    return product_query.first()

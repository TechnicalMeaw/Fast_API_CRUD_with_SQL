from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List


models.Base.metadata.create_all(bind=engine)


app = FastAPI()



while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', password='1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)



@app.get("/items", response_model=List[schemas.Product])
def test_posts(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.post("/items", status_code= status.HTTP_201_CREATED, response_model= schemas.Product)
def add_item(item : schemas.ProductCreate, db: Session = Depends(get_db)):
    new_item = models.Product(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item



@app.get("/items/{id}", response_model= schemas.Product)
def get_item(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    
    return product
    


@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    
    product.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/items/{id}", response_model= schemas.Product)
def update_item(id: int, item:schemas.ProductCreate, db: Session = Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.id == id)

    if not product_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    
    product_query.update(item.dict(), synchronize_session=False)
    db.commit()
    return product_query.first()





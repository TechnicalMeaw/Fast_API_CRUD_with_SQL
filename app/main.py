from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Item(BaseModel):
    title : str
    price: int
    inventory: int


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



@app.get("/")
def root():
    cursor.execute("""SELECT * FROM products""")
    products = cursor.fetchall()
    return {"data": products}


@app.post("/items", status_code= status.HTTP_201_CREATED)
def add_item(item : Item):
    cursor.execute("""INSERT INTO products (name, price, inventory) VALUES (%s, %s, %s) RETURNING * """, (item.title, item.price, item.inventory))
    new_item = cursor.fetchone()

    conn.commit()
    return {"data": new_item}



@app.get("/items/{id}")
def get_item(id: int, responce: Response):

    cursor.execute("""SELECT * FROM products WHERE id = %s """, (str(id),))
    product = cursor.fetchone()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    
    return {"data": product}
    


@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int):
    cursor.execute("""DELETE FROM products WHERE id = %s RETURNING * """, (str(id),))
    deleted_item = cursor.fetchone()
    conn.commit()

    if not deleted_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/items/{id}")
def update_item(id: int, item:Item):
    cursor.execute("""UPDATE products SET name = %s, price = %s, inventory = %s WHERE id = %s RETURNING *""", (item.title, item.price, item.inventory, str(id)))
    updated_item = cursor.fetchone()
    conn.commit()
    if not updated_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    
    return {"updated": id, "data" : updated_item}





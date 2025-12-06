#1. import fast api
from fastapi import FastAPI, Depends
#this is an inbuilt package in python which allows us to define the shape of POST and PATHCH methods and aslso do validations
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import get_db, User, Category, Product, Order

#create and instance
app = FastAPI()


#allow network request from all servers
app.add_middleware(CORSMiddleware, allow_origins=["*"])


#create routes and instances
@app.get("/")
def read_root():
    return {"Hello": "World"}

class UserSchema(BaseModel):
    name: str
    email: str
    role: str | None = "Employee"

#http://localhost:8000/User -> POST-> create a single genre
@app.post("/User")
def create_user():
    #use sql alchemy to create records
    return {"message":"User created succesfully"}

#http://localhost:8000/User -> GET-> retrieve all genre
@app.get("/User")
def get_user():
    #use sql alchemy to retrieve all users 
    return[]

#http://localhost:8000/User -> GET-> get a single genre
@app.get("/User/{User_id}")
def get_user(User_id):
    #retrieve a single user using sqlalchemy
    #User=db.query(User).filter(id==User_id).first()
    return{"id":User_id}

#http://localhost:8000/User -> PATCH-> update a single genre
@app.patch("/User/{User_id}")
def update_user(User_id):
    return{}

#http://localhost:8000/User -> DELETE-> create a single genre
@app.delete("/User/{User_id}")
def delete_user(User_id):
    return{}

class CategorySchema(BaseModel):
    name:str
    description: str | None=None

#http://localhost:8000/User -> POST-> create a single genre
@app.post("/Category")
def create_category(category:CategorySchema, session = Depends(get_db)):
    #check if the genre exists
    existing=session.query(Category).filter(Category.name == category.name).first()


    if existing is not None:
        return {"message":"Category already exists"}
    #print(category) #this will be a dict
    #persist to db
    #1.create an instance of category class(model)with the details
    new_category=Category(name=category.name)
    #add the instance to the transaction
    session.add(new_category)
    #3.commit the transaction
    session.commit()
    #return a message that the category has been created 
    return {"message":"Category created succesfully"}

#http://localhost:8000/User -> GET-> retrieve all genre
@app.get("/Category")
def get_category(session = Depends(get_db)):
    #use sql alchemy to retrieve all users 
    category = session.query(Category).all()
    return category

#http://localhost:8000/User -> GET-> get a single genre
@app.get("/Category/{Category_id}")
def get_category(Category_id):
    #retrieve a single user using sqlalchemy
    #User=db.query(User).filter(id==User_id).first()
    return{"id":Category_id}

#http://localhost:8000/User -> PATCH-> update a single genre
@app.patch("/Category/{Category_id}")
def update_category(Category_id):
    return{}

#http://localhost:8000/User -> DELETE-> create a single genre
@app.delete("/Category/{Category_id}")
def delete_category(Category_id):
    return{}


class ProductSchema(BaseModel):
    name: str
    price: int
    stock: int
    category_id: int
    user_id: int


#http://localhost:8000/User -> POST-> create a single genre
@app.post("/Product")
def create_product():
    #use sql alchemy to create records
    return {"message":"product created succesfully"}

#http://localhost:8000/User -> GET-> retrieve all genre
@app.get("/Product")
def get_product():
    #use sql alchemy to retrieve all users 
    return[]

#http://localhost:8000/User -> GET-> get a single genre
@app.get("/Product/{Product_id}")
def get_product(Product_id):
    #retrieve a single user using sqlalchemy
    #User=db.query(User).filter(id==User_id).first()
    return{"id":Product_id}

#http://localhost:8000/User -> PATCH-> update a single genre
@app.patch("/Product/{Product_id}")
def update_product(Product_id):
    return{}

#http://localhost:8000/User -> DELETE-> create a single genre
@app.delete("/Product/{Product_id}")
def delete_product(Product_id):
    return{}

class OrderSchema(BaseModel):
    product_id: int
    user_id: int
    quantity: int

#http://localhost:8000/User -> POST-> create a single genre
@app.post("/Order")
def create_order():
    #use sql alchemy to create records
    return {"message":"Order created succesfully"}

#http://localhost:8000/User -> GET-> retrieve all genre
@app.get("/Order")
def get_order():
    #use sql alchemy to retrieve all users 
    return[]

#http://localhost:8000/User -> GET-> get a single genre
@app.get("/Order/{Order_id}")
def get_order(Order_id):
    #retrieve a single user using sqlalchemy
    #User=db.query(User).filter(id==User_id).first()
    return{"id":Order_id}

#http://localhost:8000/User -> PATCH-> update a single genre
@app.patch("/Order/{Order_id}")
def update_order(Order_id):
    return{}

#http://localhost:8000/User -> DELETE-> create a single genre
@app.delete("/Order/{Order_id}")
def delete_order(Order_id):
    return{}
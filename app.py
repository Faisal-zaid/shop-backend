#1. import fast api
from fastapi import FastAPI, Depends
#this is an inbuilt package in python which allows us to define the shape of POST and PATHCH methods and aslso do validations
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import get_db, User, Category, Product, Order,Session

#create and instance
app = FastAPI()


#allow network request from all servers
app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_credentials=True, # Allows cookies/authentication headers
    # CRITICAL: Allow all methods (POST, PUT, PATCH, DELETE) and all headers
    allow_methods=["*"], 
    allow_headers=["*"],)


#create routes and instances
@app.get("/")
def read_root():
    return {"Hello": "World"}

class UserSchema(BaseModel):
    name: str
    email:str
    role: str 

#http://localhost:8000/User -> POST-> create a single user
@app.post("/User")
def create_user(user: UserSchema, session: Session = Depends(get_db)):

    new_user = User(
        name=user.name,
        email=user.email,
        role=user.role
    )

    session.add(new_user)
    session.commit()
    

    return {"message": "User created successfully"}
    #use sql alchemy to create records
    

#http://localhost:8000/User -> GET-> retrieve all user
@app.get("/User")
def get_user(session: Session = Depends(get_db)):
    users = session.query(User).all()
    return users


    #use sql alchemy to retrieve all users 
    

#http://localhost:8000/User -> GET-> get a single user
@app.get("/User/{User_id}")
def get_user(User_id: int, session: Session = Depends(get_db)):
    user = session.query(User).filter(User.id == User_id).first()

    if not user:
        return {"message": "User not found"}

    return user
    #retrieve a single user using sqlalchemy
    #User=db.query(User).filter(id==User_id).first()
    

#http://localhost:8000/User -> PATCH-> update a single user
@app.patch("/User/{User_id}")
def update_user(User_id: int, data: UserSchema, session: Session = Depends(get_db)):
    user = session.query(User).filter(User.id == User_id).first()

    if not user:
        return {"message": "User not found"}

    user.name = data.name
    user.role = data.role

    session.commit()
    session.refresh(user)

    return {"message": "User updated"}

#http://localhost:8000/User -> DELETE-> create a single user
@app.delete("/User/{User_id}")
def delete_user(User_id: int, session: Session = Depends(get_db)):
    user = session.query(User).filter(User.id == User_id).first()

    if not user:
        return {"message": "User not found"}

    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully"}

class CategorySchema(BaseModel):
    name:str
    description: str 

#http://localhost:8000/Category -> POST-> create a single user
@app.post("/Category")
def create_category(category:CategorySchema, session = Depends(get_db)):
    # ... (existing code to check for existence) ...

    # 1. create an instance of category class(model) with the details
    new_category=Category(
        name=category.name,
        description=category.description
        )
    # add the instance to the transaction
    session.add(new_category)
    # 3. commit the transaction
    session.commit()
    
    # 🌟 CRITICAL FIX: Refresh the object to get the generated ID
    session.refresh(new_category) 
    
    # 🌟 CRITICAL FIX: Return the newly created object, not just a message
    return new_category # <-- Return the Category object

#http://localhost:8000/Category -> GET-> retrieve all category
@app.get("/Category")
def get_category(session = Depends(get_db)):
    #use sql alchemy to retrieve all categories
    category = session.query(Category).all()
    return category

#http://localhost:8000/Category -> GET-> get a single category
@app.get("/Category/{Category_id}")
def get_category(Category_id: int, session: Session = Depends(get_db)):
    #retrieve a single category using sqlalchemy
    #User=db.query(User).filter(id==User_id).first()
     category = session.query(Category).filter(Category.id == Category_id).first()

     return {"category": category}

#http://localhost:8000/Category -> PATCH-> update a single category
@app.put("/Category/{category_id}")
def update_category(category_id: int, data: CategorySchema, session: Session = Depends(get_db)):

    category = session.query(Category).filter(Category.id == category_id).first()

    if not category:
        return {"message": "Category not found"}

    # prevent duplicate name
    if data.name:
        exists = session.query(Category).filter(Category.name == data.name, Category.id != category_id).first()
        if exists:
            return {"message": "Name already used by another category"}

    # Update fields
    if data.name:
        category.name = data.name
    if data.description is not None:
        category.description = data.description

    session.commit()
    session.refresh(category)

    return {"message": "Category updated"}




#http://localhost:8000/Category -> DELETE-> delete a single category
@app.delete("/Category/{category_id}")
def delete_category(category_id: int, session: Session = Depends(get_db)):

    category = session.query(Category).filter(Category.id == category_id).first()

    

    session.delete(category)
    session.commit()

    return {"message": "Category deleted successfully"}


class ProductSchema(BaseModel):
    name: str
    price: int
    stock: int
    category_id: int
    user_id: int


#http://localhost:8000/Product -> POST-> create a single product
@app.post("/Product")
def create_product(product: ProductSchema, session: Session = Depends(get_db)):
    # Check category exists
    category = session.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise ("Category not found")
    # Check user exists
    user = session.query(User).filter(User.id == product.user_id).first()
    if not user:
        raise ("User not found")
    new_product = Product(**product.dict())
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return {"message": "Product created successfully"}


#http://localhost:8000/Product -> GET-> retrieve all product
@app.get("/Product")
def get_product(session: Session = Depends(get_db)):
    #use sql alchemy to retrieve all users 
    return session.query(Product).all()

#http://localhost:8000/Product -> GET-> get a single product
@app.get("/Product/{Product_id}")
def get_product(Product_id: int, session: Session = Depends(get_db)):
    product = session.query(Product).filter(Product.id == Product_id).first()
    
    return product
    #retrieve a single product
    # using sqlalchemy
    #User=db.query(User).filter(id==User_id).first()
    

#http://localhost:8000/Product -> PATCH-> update a single product
@app.patch("/Product/{Product_id}")
def update_product(Product_id: int, product: ProductSchema, session: Session = Depends(get_db)):
    existing_product = session.query(Product).filter(Product.id == Product_id).first()
    if not existing_product:
        raise ("Product not found")
    for key, value in product.dict().items():
        setattr(existing_product, key, value)
    session.commit()
    session.refresh(existing_product)
    return {"message": "Product updated"}


#http://localhost:8000/Product -> DELETE-> delete a single product
@app.delete("/Product/{Product_id}")
def delete_product(Product_id: int, session: Session = Depends(get_db)):
    product = session.query(Product).filter(Product.id == Product_id).first()
    
    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully"}

class OrderSchema(BaseModel):
    product_id: int
    user_id: int
    quantity: int

#http://localhost:8000/Order -> POST-> create a single order
@app.post("/Order")
def create_order(order: OrderSchema, session: Session = Depends(get_db)):
    # Check product exists
    product = session.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise ("Product not found")
    # Check stock
    if order.quantity > product.stock:
        raise ("Not enough stock")
    # Check user exists
    user = session.query(User).filter(User.id == order.user_id).first()
    if not user:
        raise ("User not found")
    
    # Deduct stock
    product.stock -= order.quantity
    
    # Calculate total price
    total_price = order.quantity * product.price
    
    # Create order record
    new_order = Order(
        product_id=order.product_id,
        user_id=order.user_id,
        quantity=order.quantity,
        total_price=total_price
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    
    return {"message": "Order created successfully", "order": new_order, "remaining_stock": product.stock}


#http://localhost:8000/Order -> GET-> retrieve all order
@app.get("/Order")
def get_order(session: Session = Depends(get_db)):
    #use sql alchemy to retrieve all users 
     return session.query(Order).all()


#http://localhost:8000/Order -> GET-> get a single order
@app.get("/Order/{Order_id}")
def get_order(Order_id: int, session: Session = Depends(get_db)):
    order = session.query(Order).filter(Order.id == Order_id).first()
    
    return order
    #retrieve a single order using sqlalchemy
    #User=db.query(User).filter(id==User_id).first()
    

#http://localhost:8000/Order -> PATCH-> update a single order
@app.patch("/Order/{Order_id}")
def update_order(Order_id: int, order: OrderSchema, session: Session = Depends(get_db)):
    existing_order = session.query(Order).filter(Order.id == Order_id).first()
    if not existing_order:
        raise ("Order not found")
    for key, value in order.dict().items():
        setattr(existing_order, key, value)
    session.commit()
    session.refresh(existing_order)
    return {"message": "Order updated", "order": existing_order}

#http://localhost:8000/Order -> DELETE-> delete a single order
@app.delete("/Order/{Order_id}")
def delete_order(Order_id: int, session: Session = Depends(get_db)):
    order = session.query(Order).filter(Order.id == Order_id).first()
    
    session.delete(order)
    session.commit()
    return {"message": "Order deleted successfully"}
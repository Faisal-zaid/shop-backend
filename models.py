#from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer,Text,DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

#setup base class where our models will inherit from
Base=declarative_base()

#start creating the schema
class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    name = Column(Text(), nullable=False)
    email = Column(Text(), unique=True,  nullable=False)
    role = Column(Text(), default="staff")
    created_at = Column(DateTime, default=datetime. now)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, )
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now) 

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)  

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # who recorded the order
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)         

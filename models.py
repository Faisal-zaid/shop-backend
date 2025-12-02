#from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer,Text,DateTime
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

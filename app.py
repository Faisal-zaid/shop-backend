#1. import fast api
from fastapi import FastAPI

#create and instance
app = FastAPI()


#create routes and instances
@app.get("/")
def read_root():
    return {"Hello": "World"}

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
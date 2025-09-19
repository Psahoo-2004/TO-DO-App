from fastapi import FastAPI,Depends,HTTPException
from . import models,auth
from .import schemas
from app.database import engine,get_db
from sqlalchemy.orm import Session
from . utils import hashed
from .router import user,todo

app=FastAPI()

Tasks={}

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(todo.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"Hello World"}
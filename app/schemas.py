from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr
    password:str

class CreateUser(UserBase):
    pass

class UpdateUser(BaseModel):
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        from_attributes = True


class ToDo(BaseModel):
    title:str
    completed:bool = False
    # owner_id:int

class CreateToDO(ToDo):
    pass
class UpdateToDO(BaseModel):
    completed:bool=False

class ToDoOut(ToDo):
    id:int
    # task:ToDo
    created_at:datetime

    class Config:
        from_attributes = True
    
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None
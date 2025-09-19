from app.database import Base
from sqlalchemy import Column, ForeignKey,Integer,String,Boolean,TIMESTAMP,text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner=relationship("TODO")

class TODO(Base):
    __tablename__="todo"
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    completed=Column(Boolean,server_default="False",nullable=False)
    owner_id=Column(Integer,ForeignKey("user.id",ondelete="cascade"),nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

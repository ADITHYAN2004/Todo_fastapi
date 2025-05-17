from sqlmodel import SQLModel, Field, Column, DateTime, Relationship
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, Session, SQLModel, create_engine, select

class User(SQLModel ,table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username : str = Field(index=True)
    email : str =Field(unique=True, index=True)
    hashed_password : str
    todos :  List["Todo"] = Relationship(back_populates="owner")


  
class Todo(SQLModel ,table=True):
    __tablename__ = "todos"
    id: Optional[int] = Field(default=None, primary_key=True)
    title : str = Field( index=True)
    description : str
    time_to_complete :  datetime
    completed :bool =False
    owner_id : Optional[int] = Field(default=None, foreign_key="users.id")
    owner : Optional[User]= Relationship(back_populates="todos")


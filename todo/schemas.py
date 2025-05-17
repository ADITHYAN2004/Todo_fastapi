from sqlmodel import SQLModel
from typing import  List
from datetime import datetime
class UserCreate(SQLModel):
    username: str
    email: str
    password: str

class ShowUser(SQLModel):
    id: int
    username: str
    email: str

    class Config:
        from_attribute = True

class TodoCreate(SQLModel):
    title: str
    description: str
    time_to_complete: datetime

class ShowTodo(SQLModel):
    id: int
    title: str
    description: str
    time_to_complete: datetime
    completed: bool

    class Config:
        from_attribute = True

class Login(SQLModel):
    username: str
    password: str


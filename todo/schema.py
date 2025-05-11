from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class ShowUser(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class TodoCreate(BaseModel):
    title: str
    description: str
    time_to_complete: datetime

class ShowTodo(BaseModel):
    id: int
    title: str
    description: str
    time_to_complete: datetime
    completed: bool

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str


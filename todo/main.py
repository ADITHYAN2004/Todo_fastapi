from fastapi import FastAPI
from .db import models
from todo.routes import user, todo 
from .db import database
from sqlmodel import SQLModel
from .db.database import engine  




app = FastAPI()



app.include_router(user.router)
app.include_router(todo.router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

from fastapi import FastAPI
from todo.routes import user, todo 
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()



app.include_router(user.router)
app.include_router(todo.router)



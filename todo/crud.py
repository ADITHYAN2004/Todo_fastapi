from sqlalchemy.orm import Session
from todo import models, schemas, auth
from .utils import hashing
from datetime import datetime

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashing.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_user_todos(db: Session, user_id: int):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).all()

def mark_todo_complete(db: Session, todo_id: int, user_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user_id).first()
    if todo:
        todo.completed = True
        db.commit()
        return todo
    return None


def delete_todo(db: Session, todo_id: int, user_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user_id).first()
    if todo:
        db.delete(todo)
        db.commit()
        return todo
    return None


def get_user_todos_grouped(db: Session, user_id: int):
    now = datetime.utcnow()
    todos = db.query(models.Todo).filter(models.Todo.owner_id == user_id).all()

    completed = []
    pending = []
    elapsed = []

    for todo in todos:
        if todo.completed:
            completed.append(todo)
        elif todo.time_to_complete < now:
            elapsed.append(todo)
        else:
            pending.append(todo)

    return {
        "completed": completed,
        "to_be_done": pending,
        "elapsed": elapsed
    }

def update_todo(db: Session, todo_id: int, user_id: int, updated_data: schemas.TodoCreate):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user_id).first()
    if not todo:
        return None
    todo.title = updated_data.title
    todo.description = updated_data.description
    todo.time_to_complete = updated_data.time_to_complete
    db.commit()
    db.refresh(todo)
    return todo

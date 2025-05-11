from sqlalchemy.orm import Session
from todo import models, schemas, auth
from datetime import datetime

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
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

def mark_todo_complete(db: Session, todo_id: int):
    todo = db.query(models.Todo).get(todo_id)
    if todo:
        todo.completed = True
        db.commit()
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).get(todo_id)
    if todo:
        db.delete(todo)
        db.commit()
    return todo


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from todo import schemas, crud, database

router = APIRouter(prefix="/todo", tags=["Todos"])

@router.post("/")
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(database.get_db)):
    return crud.create_todo(db, todo, user_id=1)  # Replace with auth user ID later

@router.get("/")
def get_todos(db: Session = Depends(database.get_db)):
    return crud.get_user_todos(db, user_id=1)

@router.patch("/{todo_id}/complete")
def complete(todo_id: int, db: Session = Depends(database.get_db)):
    return crud.mark_todo_complete(db, todo_id)

@router.delete("/{todo_id}")
def delete(todo_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_todo(db, todo_id)

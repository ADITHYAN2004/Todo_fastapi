from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from todo import schemas, crud, auth
from ..db import database
from  ..db.models import User, Todo
from datetime import datetime
from typing import List, Dict

router = APIRouter(prefix="/todo", tags=["Todos"])


@router.post("/")
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    return crud.create_todo(db, todo, user_id=current_user.id)


@router.get("/")
def get_todos(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    
    return crud.get_todos(db, user_id=current_user.id)

@router.patch("/{todo_id}/complete")
def complete(
    todo_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    todo = crud.mark_todo_complete(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized")
    return todo

@router.delete("/{todo_id}")
def delete(
    todo_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    todo = crud.delete_todo(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized")
    return todo


@router.put("/{todo_id}")
def update_todo(
    todo_id: int,
    updated_data: schemas.TodoCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    todo = crud.update_todo(db, todo_id, current_user.id, updated_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized")
    return todo

@router.get("/todos/grouped", response_model=Dict[str, List[schemas.ShowTodo]])
def get_grouped_todos(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    todos = db.query(Todo).filter(Todo.owner_id == current_user.id).all()

    now = datetime.utcnow()
    grouped = {
        "completed": [],
        "to_be_done": [],
        "time_elapsed": []
    }

    for todo in todos:
        if todo.completed:
            grouped["completed"].append(todo)
        elif todo.time_to_complete and todo.time_to_complete< now:
            grouped["time_elapsed"].append(todo)
        else:
            grouped["to_be_done"].append(todo)

    return grouped

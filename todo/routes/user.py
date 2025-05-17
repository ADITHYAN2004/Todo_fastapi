from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from todo import schemas, crud, auth, database 
from ..utils import hashing
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Users"])

@router.post("/signup", response_model=schemas.ShowUser)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db, user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not hashing.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


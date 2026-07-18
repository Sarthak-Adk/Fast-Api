from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
import crud
import schemas

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)
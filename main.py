from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models, schemas, crud
from datetime import timedelta
from auth import create_access_token, get_current_user
from typing import List

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, FastAPI is working!"}

#---------------- User Registration -------------------
@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.register_user(db, user)

#---------------- Login (JWT Token Return) -------------------
@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=400)
    access_token = create_access_token(
        data={"sub": str(db_user.user_id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

#---------------- Profile -------------------
@app.get("/profile")
def read_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at
    }

#---------------- Tasks -------------------
@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, 
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    return crud.create_task(db, task, current_user.user_id)

@app.get("/tasks", response_model=List[schemas.Task])
def list_tasks(db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_user)):
    return crud.get_tasks(db, current_user.user_id)

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, 
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    return crud.update_task(db, task_id, task, current_user.user_id)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, 
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    crud.delete_task(db, task_id, current_user.user_id)
    return {"detail": "Task deleted successfully"}

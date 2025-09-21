from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models

# Create DB tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, FastAPI is working!"}

@app.post("/todos/")
def create_todo(title: str, description: str = "", db: Session = Depends(get_db)):
    todo = models.Todo(title=title, description=description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.get("/todos/")
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

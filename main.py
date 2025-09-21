from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models,schemas, crud

# Create DB tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, FastAPI is working!"}

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.register_user(db, user)


@app.post("/login", response_model=schemas.UserOut)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.email, user.password) # type: ignore
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_user
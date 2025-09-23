from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
import models, schemas
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#---------------- Password -----------------
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#---------------- Users -----------------
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def register_user(db: Session, user: schemas.UserRegister):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)   # hash password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating user")

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


#---------------- Tasks -----------------
def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(title=task.title, desc=task.desc, user_id=user_id)
    try:
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating task")

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.task_id == task_id).first()

def get_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate, user_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    try:
        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating task")

def delete_task(db: Session, task_id: int, user_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    try:
        db.delete(db_task)
        db.commit()
        return db_task
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting task")

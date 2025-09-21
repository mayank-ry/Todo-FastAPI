# crud.py
from sqlalchemy.orm import Session
import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first() # type: ignore

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first() # type: ignore

def register_user(db: Session, user: schemas.UserRegister):
    db_user = models.User(email=user.email, name=user.name) # type: ignore
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_item_for_user(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id) # type: ignore
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first() # type: ignore

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first() # type: ignore

def register_user(db: Session, user: schemas.UserRegister):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError:
        db.rollback()
        raise

def create_item_for_user(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id) # type: ignore
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError:
        db.rollback()
        raise

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

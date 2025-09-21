# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class ItemBase(BaseModel):
    title: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    name: str

class UserRegister(UserBase):
    email : str
    password : str
    
class UserLogin(UserBase):
    email : str
    password : str

class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True

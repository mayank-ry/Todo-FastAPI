from pydantic import BaseModel
from typing import List

class ItemBase(BaseModel):
    title: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# Base user schema
class UserBase(BaseModel):
    email: str

# For registration (input only)
class UserRegister(UserBase):
    username: str
    password: str

# For login (input only)
class UserLogin(UserBase):
    email: str
    password: str

# For output (response)
class UserOut(BaseModel):
    user_id: int
    username: str
    email: str

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class TaskBase(BaseModel):
    title: str
    desc: Optional[str] = None
    status: Optional[str] = "pending"
    priority: Optional[str] = "medium"
    due_date: Optional[date] = None
    attachment_url: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass 



class Task(TaskBase):
    task_id: int
    user_id: int

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

#token schema updated author mayank
class Token(BaseModel):
    access_token:str
    token_type:str


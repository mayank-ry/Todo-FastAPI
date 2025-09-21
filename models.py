from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Date, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

# Users Table
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationship to tasks
    tasks = relationship("Task", back_populates="user")

# Tasks Table
class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String(100), nullable=False, index=True)
    desc = Column(String, nullable=True)
    status = Column(Enum("pending", "in_progress", "completed", name="task_status"), default="pending")
    priority = Column(Enum("low", "medium", "high", name="task_priority"), default="medium")
    due_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationship to user
    user = relationship("User", back_populates="tasks")

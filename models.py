# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Example: Users table
class User(Base):
    __tablename__ = "users"  # table name in DB

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)   # unique key
    name = Column(String)

    # One-to-many relationship with items
    items = relationship("Item", back_populates="owner")

# Example: Items table
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))  # foreign key

    # Relationship back to User
    owner = relationship("User", back_populates="items")

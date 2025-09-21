# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine (talks to DB)
engine = create_engine(DATABASE_URL)

# SessionLocal: actual session class bound to engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: used for creating ORM models
Base = declarative_base()

# Dependency for getting DB session inside routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

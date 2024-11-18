# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .base import Base  # Import Base from base.py

# Load environment variables from .env file
load_dotenv()

# Fetch DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

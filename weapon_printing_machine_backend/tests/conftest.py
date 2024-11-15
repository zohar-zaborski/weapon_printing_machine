# tests/conftest.py
import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from app.base import Base  # Import Base from base.py
from app.database import get_db
from app.main import app

# Add the app directory to the system path


# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the `get_db` dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create tables in the testing database
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)  # Create tables
    yield
    Base.metadata.drop_all(bind=engine)  # Drop tables after tests

# Test client for making requests
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Fixture to populate the weapons table with test data
@pytest.fixture(scope="module")
def populate_weapons(test_db):
    db = TestingSessionLocal()  # Use the test session
    db.execute("""
        INSERT INTO weapons (id, name, compatible_parts)
        VALUES 
        (1, 'Assault Rifle', '1,2,3'),
        (2, 'Sniper Rifle', '2,4'),
        (3, 'Shotgun', '1,3,5');
    """)
    db.commit()
    db.close()


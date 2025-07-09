import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add project root to path to allow imports from the 'app' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import create_app
from app.database.models import Base
from app.routes.api import get_db

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the FastAPI app instance for testing
app = create_app()

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_db():
    """
    Fixture to create database tables once per test session and drop them after.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Provides a clean, transactional database session for each test function.
    It rolls back the transaction after the test, ensuring test isolation.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Override the app's get_db dependency to use this transactional session
    app.dependency_overrides[get_db] = lambda: session

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    
    # Clear the dependency override after the test
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def client(db_session):
    """
    A TestClient for the app that uses the transactional db_session.
    We depend on db_session to ensure the dependency override is active.
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def test_user_credentials():
    """Provides standard credentials for a test user."""
    return {"email": "test@example.com", "password": "testpassword"}

@pytest.fixture(scope="function")
def test_user(client, test_user_credentials):
    """
    Registers a new user for a test and returns their credentials.
    This runs for each test function that needs a fresh user.
    """
    response = client.post(
        "/api/v1/register",
        json={
            "email": test_user_credentials["email"],
            "password": test_user_credentials["password"],
            "confirmPassword": test_user_credentials["password"],
        },
    )
    assert response.status_code == 200, "Failed to register test user"
    return test_user_credentials

@pytest.fixture(scope="function")
def auth_token(client, test_user):
    """
    Logs in the test user and returns an authentication token.
    """
    response = client.post(
        "/api/v1/login",
        json=test_user,
    )
    assert response.status_code == 200, "Failed to log in test user"
    data = response.json()
    return data["access_token"]
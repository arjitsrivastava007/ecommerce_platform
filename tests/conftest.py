import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.v1.models.base import Base, get_db
from fastapi.testclient import TestClient
import os
from app.main import app
import psycopg2


# Get database credentials from environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
TEST_DB_NAME = os.getenv("POSTGRES_TEST_DB")
ENV = os.environ.get("ENV")
if ENV == "local":
    DB_HOST = "localhost"
else:
    DB_HOST = "db"

# Define test database connection URL
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_database():
    """Create the test database using psycopg2"""
    print("🔧 Setting up test database...")

    try:
        # Connect to PostgreSQL (default database)
        conn = psycopg2.connect(
            dbname="postgres",
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=DB_HOST,
            port="5432"
        )
        conn.autocommit = True  # Required for CREATE DATABASE
        cursor = conn.cursor()

        # Create the test database if it doesn't exist
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}';")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {TEST_DB_NAME};")
            print("✅ Test database created successfully!")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error creating test database: {e}")


def drop_test_database():
    """Drop the test database after tests using psycopg2"""
    print("🗑️ Dropping test database...")

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=DB_HOST,
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME} WITH (FORCE);")
        print("✅ Test database dropped!")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error dropping test database: {e}")


@pytest.fixture(scope="session")
def test_db():
    """Set up and teardown the test database"""
    create_test_database()
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    yield db  # Tests run here

    db.close()
    drop_test_database()


@pytest.fixture(scope="session")
def override_get_db(test_db):
    """Override FastAPI's dependency to use the test database"""

    def _get_db():
        try:
            yield test_db
        finally:
            test_db.rollback()

    app.dependency_overrides[get_db] = _get_db
    return test_db


@pytest.fixture(scope="session")
def client(override_get_db):
    """Set up test client for FastAPI"""
    with TestClient(app) as c:
        yield c

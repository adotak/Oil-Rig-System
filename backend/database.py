import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Default to Postgres localhost, allowing override via environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/oilrig"
)

# Connect arguments: check_same_thread is only for SQLite
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

try:
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    # Test the connection to trigger exception if Postgres isn't configured
    with engine.connect() as connection:
        pass
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Database connection error. Please ensure PostgreSQL is running and the database 'oilrig' exists. Error: {e}")
    # Fallback to SQLite if Postgres fails so the app doesn't crash entirely during dev
    print("Falling back to SQLite...")
    engine = create_engine("sqlite:///./oilrig.db", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

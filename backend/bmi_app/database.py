"""
Script Name : database.py
Description : Database connection logic (SQLAlchemy engine, session)
Author      : @tonybnya
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .core.config import get_settings
from .models import Base

settings = get_settings()

# Create engine with appropriate configuration
# SQLite specific configuration
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=settings.debug,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency to get database session for FastAPI routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all tables in the database.
    """
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """
    Drop all tables from the database.
    """
    Base.metadata.drop_all(bind=engine)

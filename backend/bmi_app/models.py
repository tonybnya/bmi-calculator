"""
Script Name : models.py
Description : SQLAlchemy models (User, Measurement, BMICategory)
Author      : @tonybnya
"""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """
    Define the User model.
    """
    __tablename__ == "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationship to measurements
    measurements = relationship("Measurement", back_populates="user")


class BMICategory(Base):
    """
    Define the BMI Category model.
    """
    __tablename__ == "bmi_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    min_value = Column(Float, nullable=True)
    max_value = Column(Float, nullable=True)

    measurements = relationship("Measurement", back_populates="category")

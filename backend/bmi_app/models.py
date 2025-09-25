"""
Script Name : models.py
Description : SQLAlchemy models (User, Measurement, BMICategory)
Author      : @tonybnya
"""
import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (Column, DateTime, Enum, Float, ForeignKey, Integer,
                        String, Text)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class WeightUnit(enum.Enum):
    """
    Weight unit options.
    """
    KB = "kg"
    LB = "lb"


class HeightUnit(enum.Enum):
    """
    Height unit options.
    """
    M = "m"
    CM = "cm"
    IN = "in"


class User(Base):
    """
    Define the User model.
    """
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
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


class Category(Base):
    """
    Define the BMI Category model.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    min_value = Column(Float, nullable=True)
    max_value = Column(Float, nullable=True)

    measurements = relationship("Measurement", back_populates="category")


class Measurement(Base):
    """
    Define the Measurement model.
    """
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    category_id = Column(
        Integer,
        ForeignKey("bmi_categories_id"),
        nullable=False
    )

    height = Column(Float, nullable=False)
    height_unit = Column(Enum(HeightUnit), nullable=False, default=HeightUnit.M)
    weight = Column(Float, nullable=False)
    weight_unit = Column(Enum(WeightUnit), nullable=False, default=WeightUnit.KG)

    height_m = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)

    recorded_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    notes = Column(Text, nullable=True)

    # Relationship back to User
    user = relationship("User", back_populates="measurements")
    # Relationship back to Category
    category = relationship("Category", back_populates="measurements")

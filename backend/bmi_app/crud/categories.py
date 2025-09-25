"""
CRUD operations for BMI categories.
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models import Category


def get_categories(db: Session) -> List[Category]:
    """
    Retrieve all BMI categories from the database.
    """
    return db.query(Category).order_by(Category.min_value).all()


def get_category_by_id(db: Session, category_id: int) -> Optional[Category]:
    """
    Retrieve a specific category by ID.
    """
    return db.query(Category).filter(Category.id == category_id).first()

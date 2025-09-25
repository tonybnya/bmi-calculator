"""
CRUD operations for BMI categories.
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models import Category
from ..schemas import Category as CategorySchema


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


def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    """
    Retrieve a category by name.
    """
    return db.query(Category).filter(Category.name == name).first()


def get_category_by_bmi(db: Session, bmi_value: float) -> Optional[Category]:
    """
    Find the appropriate category for a given BMI value.
    """
    # Handle the case where min_value is None (underweight)
    underweight = db.query(Category).filter(
        Category.min_value.is_(None),
        Category.max_value >= bmi_value
    ).first()
    if underweight:
        return underweight

    # Handle the case where max_value is None (highest obesity class)
    obesity_extreme = db.query(Category).filter(
        Category.min_value <= bmi_value,
        Category.max_value.is_(None)
    ).first()
    if obesity_extreme:
        return obesity_extreme

    # Handle normal cases with both min and max values
    return db.query(Category).filter(
        Category.min_value <= bmi_value,
        Category.max_value > bmi_value
    ).first()


def create_category(db: Session, category: CategorySchema) -> Category:
    """
    Create a new BMI category.
    """
    db_category = Category(
        name=category.name,
        min_value=category.min_value,
        max_value=category.max_value
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(
    db: Session, 
    category_id: int, 
    category_update: CategorySchema
) -> Optional[Category]:
    """
    Update an existing category.
    """
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db_category.name = category_update.name
        db_category.min_value = category_update.min_value
        db_category.max_value = category_update.max_value
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int) -> bool:
    """
    Delete a category by ID.
    """
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False

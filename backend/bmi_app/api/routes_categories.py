"""
Script Name : routes_categories.py
Description : Endpoints for BMI categories management
Author      : @tonybnya
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from bmi_app.crud import get_categories, get_category_by_id
from bmi_app.database import get_db
from bmi_app.schemas import CategoriesResponse, Category

router = APIRouter()


@router.get("/", response_model=CategoriesResponse)
def read_categories(db: Session = Depends(get_db)):
    """
    Get all BMI categories from the database.
    """
    db_categories = get_categories(db)

    # Convert SQLAlchemy models to Pydantic schemas
    categories = [
        Category(
            name=category.name,
            min_value=category.min_value,
            max_value=category.max_value
        )
        for category in db_categories
    ]

    return CategoriesResponse(categories=categories)


@router.get("/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get a specific BMI category by ID.
    """
    db_category = get_category_by_id(db, category_id)

    if db_category is None:
        raise HTTPException(
            status_code=404,
            detail=f"Category with id {category_id} not found"
        )

    return Category(
        name=db_category.name,
        min_value=db_category.min_value,
        max_value=db_category.max_value
    )

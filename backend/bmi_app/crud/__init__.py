"""
Script Name : __init__.py
Description : CRUD operations package
Author      : @tonybnya

This package provides database CRUD operations for all models.
Import functions from specific modules or use the convenient imports below.
"""

# Category CRUD operations
from .categories import (
    get_categories,
    get_category_by_id,
    get_category_by_name,
    get_category_by_bmi,
    create_category,
    update_category,
    delete_category,
)

# User CRUD operations
from .users import (
    get_users,
    get_user_by_id,
    get_user_by_email,
    get_user_by_username,
    create_user,
    update_user,
    delete_user,
    user_exists,
)

# Measurement CRUD operations
from .measurements import (
    get_measurements,
    get_measurement_by_id,
    get_measurements_by_user,
    get_measurements_by_user_and_date_range,
    get_latest_measurement_by_user,
    create_measurement,
    update_measurement,
    delete_measurement,
    get_measurements_by_category,
    get_user_measurement_stats,
)

__all__ = [
    # Categories
    "get_categories",
    "get_category_by_id",
    "get_category_by_name",
    "get_category_by_bmi",
    "create_category",
    "update_category",
    "delete_category",
    # Users
    "get_users",
    "get_user_by_id",
    "get_user_by_email",
    "get_user_by_username",
    "create_user",
    "update_user",
    "delete_user",
    "user_exists",
    # Measurements
    "get_measurements",
    "get_measurement_by_id",
    "get_measurements_by_user",
    "get_measurements_by_user_and_date_range",
    "get_latest_measurement_by_user",
    "create_measurement",
    "update_measurement",
    "delete_measurement",
    "get_measurements_by_category",
    "get_user_measurement_stats",
]

"""
CRUD operations for measurements.
"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models import Measurement


def get_measurements(db: Session, skip: int = 0, limit: int = 100) -> List[Measurement]:
    """
    Retrieve all measurements with pagination.
    """
    return db.query(Measurement).order_by(
        Measurement.recorded_at.desc()
    ).offset(skip).limit(limit).all()


def get_measurement_by_id(db: Session, measurement_id: int) -> Optional[Measurement]:
    """
    Retrieve a measurement by ID.
    """
    return db.query(Measurement).filter(Measurement.id == measurement_id).first()


def get_measurements_by_user(
    db: Session, 
    user_id: str, 
    limit: int = 100,
    skip: int = 0
) -> List[Measurement]:
    """
    Retrieve measurements for a specific user.
    """
    return db.query(Measurement).filter(
        Measurement.user_id == user_id
    ).order_by(Measurement.recorded_at.desc()).offset(skip).limit(limit).all()


def get_measurements_by_user_and_date_range(
    db: Session,
    user_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100
) -> List[Measurement]:
    """
    Retrieve measurements for a user within a date range.
    """
    query = db.query(Measurement).filter(Measurement.user_id == user_id)

    if start_date:
        query = query.filter(Measurement.recorded_at >= start_date)
    if end_date:
        query = query.filter(Measurement.recorded_at <= end_date)

    return query.order_by(Measurement.recorded_at.desc()).limit(limit).all()


def get_latest_measurement_by_user(db: Session, user_id: str) -> Optional[Measurement]:
    """
    Get the most recent measurement for a user.
    """
    return db.query(Measurement).filter(
        Measurement.user_id == user_id
    ).order_by(Measurement.recorded_at.desc()).first()


def create_measurement(db: Session, measurement_data: dict) -> Measurement:
    """
    Create a new measurement record.
    """
    db_measurement = Measurement(**measurement_data)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement


def update_measurement(
    db: Session,
    measurement_id: int,
    measurement_data: dict
) -> Optional[Measurement]:
    """
    Update an existing measurement.
    """
    db_measurement = get_measurement_by_id(db, measurement_id)
    if db_measurement:
        for key, value in measurement_data.items():
            if hasattr(db_measurement, key):
                setattr(db_measurement, key, value)

        db.commit()
        db.refresh(db_measurement)
    return db_measurement


def delete_measurement(db: Session, measurement_id: int) -> bool:
    """
    Delete a measurement by ID.
    """
    db_measurement = get_measurement_by_id(db, measurement_id)
    if db_measurement:
        db.delete(db_measurement)
        db.commit()
        return True
    return False


def get_measurements_by_category(
    db: Session,
    category_id: int,
    limit: int = 100
) -> List[Measurement]:
    """
    Get measurements by BMI category.
    """
    return db.query(Measurement).filter(
        Measurement.category_id == category_id
    ).order_by(Measurement.recorded_at.desc()).limit(limit).all()


def get_user_measurement_stats(db: Session, user_id: str) -> dict:
    """
    Get statistics about user's measurements.
    """
    measurements = db.query(Measurement).filter(
        Measurement.user_id == user_id
    ).all()

    if not measurements:
        return {
            "total_measurements": 0,
            "avg_bmi": None,
            "min_bmi": None,
            "max_bmi": None,
            "latest_bmi": None
        }

    bmis = [m.bmi for m in measurements]

    return {
        "total_measurements": len(measurements),
        "avg_bmi": sum(bmis) / len(bmis),
        "min_bmi": min(bmis),
        "max_bmi": max(bmis),
        "latest_bmi": measurements[0].bmi if measurements else None
    }

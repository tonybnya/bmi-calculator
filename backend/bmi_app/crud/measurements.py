"""
CRUD operations for measurements.
"""
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

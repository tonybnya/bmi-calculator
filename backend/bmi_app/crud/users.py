"""
CRUD operations for users.
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models import User


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieve users with pagination.
    """
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """
    Retrieve a user by ID.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by email.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Retrieve a user by username.
    """
    return db.query(User).filter(User.username == username).first()


def create_user(
    db: Session, 
    username: str, 
    email: str, 
    password_hash: str
) -> User:
    """
    Create a new user.
    """
    db_user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session, 
    user_id: str, 
    username: Optional[str] = None,
    email: Optional[str] = None,
    password_hash: Optional[str] = None
) -> Optional[User]:
    """
    Update an existing user.
    """
    db_user = get_user_by_id(db, user_id)
    if db_user:
        if username is not None:
            db_user.username = username
        if email is not None:
            db_user.email = email
        if password_hash is not None:
            db_user.password_hash = password_hash

        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str) -> bool:
    """
    Delete a user by ID.
    """
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def user_exists(db: Session, username: str = None, email: str = None) -> bool:
    """
    Check if a user exists by username or email.
    """
    if username:
        return db.query(User).filter(User.username == username).first() is not None
    if email:
        return db.query(User).filter(User.email == email).first() is not None
    return False

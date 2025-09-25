"""
Script Name : init_db.py
Description : Script to initialize/migrate the database schema
Author      : @tonybnya
"""
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy.exc import IntegrityError

from bmi_app.database import SessionLocal, create_tables, drop_tables, engine
from bmi_app.models import Category


def init_bmi_categories():
    """
    Initialize the BMI categories table with standard BMI ranges.
    """
    db = SessionLocal()
    try:
        # Standard BMI categories
        categories_data = [
            # {"name": "Underweight", "min_value": 0.0, "max_value": 18.4},
            # {"name": "Normal weight", "min_value": 18.5, "max_value": 24.9},
            # {"name": "Overweight", "min_value": 25.0, "max_value": 29.9},
            # {"name": "Obesity Class 1", "min_value": 30.0, "max_value": 34.9},
            # {"name": "Obesity Class 2", "min_value": 35.0, "max_value": 39.9},
            # {"name": "Obesity Class 3", "min_value": 40.0, "max_value": None},
            #
            {"name": "Underweight", "min_value": None, "max_value": 18.5},
            {"name": "Normal", "min_value": 18.5, "max_value": 25},
            {"name": "Overweight", "min_value": 25, "max_value": 30},
            {"name": "Obesity I", "min_value": 30, "max_value": 35},
            {"name": "Obesity II", "min_value": 35, "max_value": 40},
            {"name": "Obesity III", "min_value": 40, "max_value": None}
        ]

        for category_data in categories_data:
            # Check if category already exists
            existing_category = db.query(Category).filter(
                Category.name == category_data["name"]
            ).first()

            if not existing_category:
                category = Category(**category_data)
                db.add(category)
                print(f"Added BMI category: {category_data['name']}")

        db.commit()
        print("BMI categories initialized successfully!")

    except IntegrityError as e:
        print(f"Error initializing BMI categories: {e}")
        db.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")
        db.rollback()
    finally:
        db.close()


def create_database():
    """
    Create all database tables.
    """
    try:
        print("Creating database tables...")
        create_tables()
        print("Database tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating database tables: {e}")
        return False


def reset_database():
    """
    Drop all tables and recreate them (USE WITH CAUTION).
    """
    try:
        print("WARNING: This will delete all data!")
        confirm = input("Are you sure you want to reset the database? (yes/no): ")
        if confirm.lower() == 'yes':
            print("Dropping all tables...")
            drop_tables()
            print("Creating tables...")
            create_tables()
            print("Database reset successfully!")
            return True
        else:
            print("Database reset cancelled.")
            return False
    except Exception as e:
        print(f"Error resetting database: {e}")
        return False


def main():
    """
    Main function to initialize the database.
    """
    print("BMI Calculator Database Initialization")
    print("=" * 40)

    # Check database connection
    try:
        with engine.connect() as conn:
            print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

    # Create tables
    if create_database():
        print("✓ Database schema created")
    else:
        print("✗ Failed to create database schema")
        return False

    # Initialize BMI categories
    init_bmi_categories()
    print("✓ Initial data populated")

    print("\nDatabase initialization completed successfully!")
    print("\nYou can now start your FastAPI application.")
    return True


if __name__ == "__main__":
    # Command line options
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "reset":
            reset_database()
        elif command == "categories":
            init_bmi_categories()
        elif command == "tables":
            create_database()
        else:
            print("Available commands:")
            print("  python init_db.py         - Full initialization")
            print("  python init_db.py reset   - Reset database (delete all data)")
            print("  python init_db.py tables  - Create tables only")
            print("  python init_db.py categories - Initialize BMI categories only")
    else:
        main()

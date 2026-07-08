"""
Database migration script to add social media link columns.

This script adds linkedin, github, and portfolio columns to the candidate_profiles table.
Run this if you have an existing database that needs to be updated with the new columns.

Usage:
    python scripts/migrate_add_social_links.py
"""
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text

from pages.core.database import db


def migrate_database():
    """Add new social link columns to candidate_profiles table."""
    print("Starting database migration: Adding social link columns...")
    
    try:
        with db.SessionLocal() as session:
            # Check if columns already exist
            inspector = db.engine.dialect
            
            columns_to_add = [
                ("linkedin", "VARCHAR(500)"),
                ("github", "VARCHAR(500)"),
                ("portfolio", "VARCHAR(500)")
            ]
            
            for column_name, column_type in columns_to_add:
                try:
                    # Try to add the column
                    alter_query = text(
                        f"ALTER TABLE candidate_profiles ADD COLUMN {column_name} {column_type}"
                    )
                    session.execute(alter_query)
                    session.commit()
                    print(f"✓ Added column: {column_name}")
                    
                except Exception as e:
                    # Column might already exist
                    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                        print(f"- Column {column_name} already exists, skipping...")
                        session.rollback()
                    else:
                        print(f"✗ Error adding column {column_name}: {e}")
                        session.rollback()
                        raise
            
            print("\n✓ Migration completed successfully!")
            print("\nThe candidate_profiles table now includes:")
            print("  - linkedin (VARCHAR 500)")
            print("  - github (VARCHAR 500)")
            print("  - portfolio (VARCHAR 500)")
            
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        raise
    finally:
        db.engine.dispose()


if __name__ == "__main__":
    print("="*60)
    print("DATABASE MIGRATION: Add Social Links")
    print("="*60)
    print("\nThis will add linkedin, github, and portfolio columns")
    print("to the candidate_profiles table.\n")
    
    response = input("Continue? (y/n): ").strip().lower()
    
    if response == 'y':
        migrate_database()
    else:
        print("Migration cancelled.")

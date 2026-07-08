"""
Automatic database migration script.
Adds social link columns to existing database without confirmation prompt.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text, inspect

from pages.core.database import db


def check_column_exists(engine, table_name, column_name):
    """Check if a column exists in a table."""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns


def add_columns_sqlite():
    """Add columns to SQLite database."""
    print("\n🔍 Checking database type: SQLite")
    
    columns_to_add = [
        ("linkedin", "VARCHAR(500)"),
        ("github", "VARCHAR(500)"),
        ("portfolio", "VARCHAR(500)")
    ]
    
    added = []
    existing = []
    
    with db.SessionLocal() as session:
        for column_name, column_type in columns_to_add:
            # Check if column exists
            if check_column_exists(db.engine, 'candidate_profiles', column_name):
                existing.append(column_name)
                print(f"  ⏭️  Column '{column_name}' already exists - skipping")
                continue
            
            try:
                # Add column to SQLite
                query = text(f"ALTER TABLE candidate_profiles ADD COLUMN {column_name} {column_type}")
                session.execute(query)
                session.commit()
                added.append(column_name)
                print(f"  ✅ Added column: {column_name}")
            except Exception as e:
                session.rollback()
                if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                    existing.append(column_name)
                    print(f"  ⏭️  Column '{column_name}' already exists - skipping")
                else:
                    print(f"  ❌ Error adding column '{column_name}': {e}")
                    raise
    
    return added, existing


def add_columns_mysql():
    """Add columns to MySQL database."""
    print("\n🔍 Checking database type: MySQL")
    
    columns_to_add = [
        ("linkedin", "VARCHAR(500)"),
        ("github", "VARCHAR(500)"),
        ("portfolio", "VARCHAR(500)")
    ]
    
    added = []
    existing = []
    
    with db.SessionLocal() as session:
        for column_name, column_type in columns_to_add:
            # Check if column exists
            if check_column_exists(db.engine, 'candidate_profiles', column_name):
                existing.append(column_name)
                print(f"  ⏭️  Column '{column_name}' already exists - skipping")
                continue
            
            try:
                # Add column to MySQL
                query = text(f"ALTER TABLE candidate_profiles ADD COLUMN {column_name} {column_type}")
                session.execute(query)
                session.commit()
                added.append(column_name)
                print(f"  ✅ Added column: {column_name}")
            except Exception as e:
                session.rollback()
                if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                    existing.append(column_name)
                    print(f"  ⏭️  Column '{column_name}' already exists - skipping")
                else:
                    print(f"  ❌ Error adding column '{column_name}': {e}")
                    raise
    
    return added, existing


def main():
    """Run the automatic migration."""
    print("=" * 70)
    print("AUTOMATIC DATABASE MIGRATION")
    print("=" * 70)
    print("\nAdding social link columns to candidate_profiles table...")
    
    try:
        # Detect database type
        db_url = str(db.engine.url)
        
        if db_url.startswith("sqlite"):
            added, existing = add_columns_sqlite()
        elif db_url.startswith("mysql"):
            added, existing = add_columns_mysql()
        else:
            print(f"\n❌ Unsupported database type: {db_url}")
            return
        
        # Summary
        print("\n" + "=" * 70)
        print("MIGRATION SUMMARY")
        print("=" * 70)
        
        if added:
            print(f"\n✅ Successfully added {len(added)} column(s):")
            for col in added:
                print(f"   - {col}")
        
        if existing:
            print(f"\n⏭️  {len(existing)} column(s) already existed:")
            for col in existing:
                print(f"   - {col}")
        
        if not added and not existing:
            print("\n⚠️  No changes made")
        else:
            print("\n✅ Migration completed successfully!")
        
        print("\nThe candidate_profiles table now includes:")
        print("  • linkedin (VARCHAR 500)")
        print("  • github (VARCHAR 500)")
        print("  • portfolio (VARCHAR 500)")
        print("\n" + "=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.engine.dispose()


if __name__ == "__main__":
    main()

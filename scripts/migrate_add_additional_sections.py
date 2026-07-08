"""
Migration script to add additional_sections_json column to candidate_profiles table.
This allows storing dynamic sections found in resumes.
"""

import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text, inspect
from pages.core.database.db import engine

def migrate():
    """Add additional_sections_json column if it doesn't exist."""
    
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('candidate_profiles')]
    
    if 'additional_sections_json' not in columns:
        print("Adding additional_sections_json column...")
        with engine.connect() as conn:
            conn.execute(text("""
                ALTER TABLE candidate_profiles 
                ADD COLUMN additional_sections_json TEXT
            """))
            conn.commit()
        print("✅ Column added successfully!")
    else:
        print("ℹ️  Column additional_sections_json already exists. No migration needed.")
    
    print("\n✅ Migration completed!")

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

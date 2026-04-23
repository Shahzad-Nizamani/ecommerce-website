#!/usr/bin/env python
"""
Migration script to create the users table.
Run this script once to initialize the database schema.
"""

import sys
from src.database.db_config import Base, engine
from src.models.product import Product
from src.models.user import User

def run_migrations():
    """Create all tables defined in models."""
    print("Starting database migration...")
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database migration completed successfully!")
        print("✓ Tables created: users, products")
        return True
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)

#!/usr/bin/env python
"""
Script to create a demo admin user for testing.
"""

import sys
from src.database.user_queries import create_user

def create_demo_user():
    """Create demo admin user."""
    print("Creating demo admin user...")
    result = create_user(
        username="admin",
        email="admin@example.com",
        password="admin",
        is_admin=True
    )
    
    if result["success"]:
        print("✓ Demo admin user created successfully!")
        print("  Username: admin")
        print("  Password: admin")
        print("  Email: admin@example.com")
        return True
    else:
        print(f"✗ Failed to create demo user: {result.get('error', 'Unknown error')}")
        return False

if __name__ == "__main__":
    success = create_demo_user()
    sys.exit(0 if success else 1)

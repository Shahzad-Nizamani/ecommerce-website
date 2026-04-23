from sqlalchemy import text
from src.database.db_config import SessionLocal
from src.utils.auth import hash_password, verify_password


def create_user(username: str, email: str, password: str, is_admin: bool = False) -> dict:
    """Create a new user in the database."""
    db_session = SessionLocal()
    try:
        # Check if user already exists
        existing = db_session.execute(
            text("SELECT id FROM users WHERE username = :username OR email = :email"),
            {"username": username, "email": email},
        ).first()
        
        if existing:
            return {"success": False, "error": "Username or email already exists"}
        
        # Hash the password
        password_hash = hash_password(password)
        
        # Insert new user
        db_session.execute(
            text("""
                INSERT INTO users (username, email, password_hash, is_admin)
                VALUES (:username, :email, :password_hash, :is_admin)
            """),
            {
                "username": username,
                "email": email,
                "password_hash": password_hash,
                "is_admin": is_admin,
            },
        )
        db_session.commit()
        return {"success": True, "message": "User created successfully"}
    except Exception as e:
        db_session.rollback()
        print(f"Error creating user: {e}")
        return {"success": False, "error": str(e)}
    finally:
        db_session.close()


def get_user_by_username(username: str) -> dict:
    """Get user by username."""
    db_session = SessionLocal()
    try:
        result = db_session.execute(
            text("SELECT id, username, email, password_hash, is_admin FROM users WHERE username = :username"),
            {"username": username},
        ).mappings().first()
        return dict(result) if result else None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        db_session.close()


def get_user_by_email(email: str) -> dict:
    """Get user by email."""
    db_session = SessionLocal()
    try:
        result = db_session.execute(
            text("SELECT id, username, email, password_hash, is_admin FROM users WHERE email = :email"),
            {"email": email},
        ).mappings().first()
        return dict(result) if result else None
    except Exception as e:
        print(f"Error fetching user by email: {e}")
        return None
    finally:
        db_session.close()


def verify_user_credentials(username: str, password: str) -> dict:
    """Verify user credentials."""
    user = get_user_by_username(username)
    
    if not user:
        return {"success": False, "user": None}
    
    if verify_password(password, user["password_hash"]):
        return {"success": True, "user": user}
    else:
        return {"success": False, "user": None}

from sqlalchemy import text
from src.database.db_config import SessionLocal


def featured_products(limit: int = 5):
    db_session = SessionLocal()
    try:
        result = db_session.execute(
            text("SELECT id, name, image, price FROM products ORDER BY RANDOM() LIMIT :limit"),
            {"limit": limit},
        ).mappings()
        return list(result)
    except Exception as e:
        print(f"Error fetching featured products: {e}")
        return []
    finally:
        db_session.close()

def recomended_products(limit: int = 10):
    db_session = SessionLocal()
    try:
        result = db_session.execute(
            text("SELECT id, name, image, price FROM products ORDER BY RANDOM() LIMIT :limit"),
            {"limit": limit},
        ).mappings()
        return list(result)
    except Exception as e:
        print(f"Error fetching recommended products: {e}")
        return []
    finally:
        db_session.close()
        
def products_by_type(type: str, limit: int = 4):
    db_session = SessionLocal()
    try:
        result = db_session.execute(
            text("SELECT id, name, image, price FROM products WHERE type = :type ORDER BY RANDOM() LIMIT :limit"),
            {"type": type, "limit": limit},
        ).mappings()
        return list(result)
    except Exception as e:
        print(f"Error fetching products by type: {e}")
        return []
    finally:
        db_session.close()

def search_products(keyword: str):
    db_session = SessionLocal()
    try:
        normalized_keyword = keyword.strip().lower()
        search_term = f"%{normalized_keyword}%"
        result = db_session.execute(
            text(
                """
                SELECT id, name, image, price, category
                FROM products
                WHERE LOWER(name) LIKE :keyword
                   OR LOWER(category) LIKE :keyword
                ORDER BY name ASC
               
                """
            ),
            {"keyword": search_term},
        ).mappings()
        return list(result)
    except Exception as e:
        print(f"Error searching products: {e}")
        return []
    finally:
        db_session.close()

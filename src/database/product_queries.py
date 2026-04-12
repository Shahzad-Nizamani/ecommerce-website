from sqlalchemy import text
from src.database.db_config import SessionLocal

def get_all_products():
    db_session = SessionLocal()
    try:
        result = db_session.execute(
            text(
                """
                SELECT id, name, image, price, category, description, stock
                FROM products
                """
            )
        ).mappings()
        return list(result)
    except Exception as e:
        print(f"Error fetching all products: {e}")
        return []
    finally:
        db_session.close()

def get_single_product(product_id: int):
    db_session = SessionLocal()
    try:
        result = db_session.execute(
            text("SELECT * FROM products WHERE id = :product_id"),
            {"product_id": product_id},
        ).mappings().first()
        return result
    except Exception as e:
        print(f"Error fetching product details: {e}")
        return None
    finally:
        db_session.close()
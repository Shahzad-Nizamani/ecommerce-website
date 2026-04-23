from sqlalchemy import text
from src.database.db_config import SessionLocal


def add_product(name: str, price: float, category: str, description: str, stock: int, image: str = None) -> dict:
    """Add a new product to the database."""
    db_session = SessionLocal()
    try:
        # Insert new product
        result = db_session.execute(
            text("""
                INSERT INTO products (name, price, category, description, stock, image)
                VALUES (:name, :price, :category, :description, :stock, :image)
                RETURNING id
            """),
            {
                "name": name,
                "price": price,
                "category": category,
                "description": description,
                "stock": stock,
                "image": image or "/assets/shoes.svg",
            },
        )
        db_session.commit()
        product_id = result.scalar()
        return {"success": True, "product_id": product_id, "message": "Product added successfully"}
    except Exception as e:
        db_session.rollback()
        print(f"Error adding product: {e}")
        return {"success": False, "error": str(e)}
    finally:
        db_session.close()

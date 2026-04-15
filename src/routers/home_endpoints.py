from fastapi import APIRouter, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from src.database.db_config import SessionLocal
from src.database.home_queries import featured_products, recomended_products, products_by_type, search_products

router = APIRouter()
templates = Jinja2Templates(directory="src/views")


@router.get("/featured_products")
def get_featured_products():
	return featured_products()

@router.get("/products_by_type/{type}")
def get_products_by_type(type: str):
	return products_by_type(type=type)

@router.get("/recommended_products")
def get_recommended_products():
	return recomended_products()

@router.get("/search")
def api_search_products(q: str = Query(...), limit: int = Query(20)):
	q = q.strip()
	normalized_query = q.lower()
	limit = max(1, min(limit, 100))
	
	if not q:
		return {"total": 0, "query": "", "products": []}
	
	products = search_products(keyword=normalized_query, limit=limit)
	
	return {
		"total": len(products),
		"query": q,
		"products": products,
	}

@router.get("/categories")
def get_categories():
    db_session = SessionLocal()
    try:
        result = db_session.execute(
            text("SELECT DISTINCT category from products WHERE category IS NOT NULL ORDER BY category")
        ).fetchall()
        return [row[0] for row in result]
    finally:
        db_session.close()
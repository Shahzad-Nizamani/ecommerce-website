from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

from src.database.home_queries import featured_products, recomended_products, products_by_type

router = APIRouter()
templates = Jinja2Templates(directory="src/views")


@router.get("/featured_products")
@router.get("/api/featured_products")
def get_featured_products(request: Request):
	return featured_products()

@router.get("/products_by_type/{type}")
@router.get("/api/products_by_type/{type}")
def get_products_by_type(request: Request, type: str):
	return products_by_type(type=type)

@router.get("/recommended_products")
@router.get("/api/recommended_products")
def get_recommended_products(request: Request):
	return recomended_products()
from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/views")

PRODUCTS = [
	{
		"id": 1,
		"name": "AeroFlex Running Shoes",
		"price": 79.99,
		"category": "Footwear",
		"image": "/assets/shoes.svg",
		"description": "Lightweight daily trainers built for comfort and speed.",
	},
	{
		"id": 2,
		"name": "Nimbus Smart Watch",
		"price": 129.00,
		"category": "Wearables",
		"image": "/assets/watch.svg",
		"description": "Track fitness goals and notifications with all-day battery life.",
	},
	{
		"id": 3,
		"name": "Urban Sling Bag",
		"price": 49.50,
		"category": "Accessories",
		"image": "/assets/bag.svg",
		"description": "Compact carry bag with quick-access pockets and durable fabric.",
	},
	{
		"id": 4,
		"name": "Echo Wireless Earbuds",
		"price": 59.00,
		"category": "Audio",
		"image": "/assets/earbuds.svg",
		"description": "Crisp sound and noise isolation in a pocket-friendly case.",
	},
]


@router.get("/")
def home(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="home.html",
		context={"featured": PRODUCTS[:4], "products_count": len(PRODUCTS)},
	)


@router.get("/products")
def product_listing(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="products.html",
		context={"products": PRODUCTS},
	)


@router.get("/products/{product_id}")
def product_details(request: Request, product_id: int):
	product = next((item for item in PRODUCTS if item["id"] == product_id), None)
	if product is None:
		raise HTTPException(status_code=404, detail="Product not found")

	return templates.TemplateResponse(
		request=request,
		name="product-details.html",
		context={"product": product},
	)

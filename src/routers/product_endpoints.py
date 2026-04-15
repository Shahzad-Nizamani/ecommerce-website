from math import ceil

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

from src.database.product_queries import get_all_products, get_single_product
from src.database.home_queries import search_products

router = APIRouter()
templates = Jinja2Templates(directory="src/views")


def _to_product_dict(item):
	product = dict(item)
	price = float(product.get("price") or 0)
	product.setdefault("id", 0)
	product.setdefault("name", "Unknown product")
	product.setdefault("image", "/assets/shoes.svg")
	product.setdefault("category", "General")
	product.setdefault("description", "No description available.")
	product.setdefault("stock", 0)
	product.setdefault("old_price", round(price * 1.18, 2))
	product.setdefault("rating", 4.2)
	product.setdefault("reviews", 12)
	product.setdefault("orders", 40)
	product.setdefault("stock_label", "In stock" if product.get("stock", 0) > 0 else "Out of stock")
	product.setdefault("material", "N/A")
	product.setdefault("design", "Standard")
	product.setdefault("sizes", ["Standard"])
	product.setdefault("seller_initial", "S")
	product.setdefault("supplier", "Brand Supplier")
	product.setdefault("location", "Germany, Berlin")
	product.setdefault("shipping", "Worldwide shipping")
	product.setdefault(
		"price_tiers",
		[
			{"label": "50-100 pcs", "amount": round(price, 2), "accent": True},
			{"label": "100-700 pcs", "amount": round(price * 0.94, 2), "accent": False},
			{"label": "700+ pcs", "amount": round(price * 0.88, 2), "accent": False},
		],
	)
	product.setdefault(
		"specs",
		[
			{"label": "Model", "value": f"# {product['id']}"},
			{"label": "Style", "value": product["category"]},
			{"label": "Certificate", "value": "N/A"},
			{"label": "Size", "value": "Standard"},
			{"label": "Memory", "value": "N/A"},
		],
	)
	product.setdefault(
		"features",
		[
			"Quality-tested product",
			"Suitable for daily use",
			"Secure packaging",
			"Customer support available",
		],
	)
	return product

@router.get("/products")
def product_listing(request: Request):
	q = (request.query_params.get("q") or "").strip().lower()
	category = (request.query_params.get("category") or "").strip().lower()
	page = max(int(request.query_params.get("page") or 1), 1)
	page_size = 6

	if q:
		raw_products = search_products(keyword=q)
	else:
		raw_products = get_all_products()

	all_products = [_to_product_dict(item) for item in raw_products]

	filtered_products = [
		item for item in all_products
		if not category or item["category"].lower() == category
	]

	total_pages = max(1, ceil(len(filtered_products) / page_size)) if filtered_products else 1
	active_page = min(page, total_pages)
	page_start = (active_page - 1) * page_size
	page_products = filtered_products[page_start : page_start + page_size]

	active_filters = [value for value in [q, category] if value]
	page_numbers = list(range(1, min(total_pages, 5) + 1))

	return templates.TemplateResponse(
		request=request,
		name="products.html",
		context={
			"products": page_products,
			"all_products": all_products,
			"query": q,
			"category": category,
			"active_filters": active_filters,
			"active_page": active_page,
			"total_pages": total_pages,
			"page_numbers": page_numbers,
			"featured_categories": [
				"Mobile accessory",
				"Electronics",
				"Smartphones",
				"Modern tech",
			],
			"brands": ["Samsung", "Apple", "Huawei", "Pocco", "Lenovo"],
			"features": ["Metallic", "Plastic cover", "8GB RAM", "Super power", "Large Memory"],
			"conditions": ["Any", "Refurbished", "Brand new", "Old items"],
			"ratings": [5, 4, 3, 2],
		},
	)


@router.get("/products/{product_id}")
def product_details(request: Request, product_id: int):
	all_products = [_to_product_dict(item) for item in get_all_products()]
	product_row = get_single_product(product_id)
	product = _to_product_dict(product_row) if product_row else None
	if product is None:
		raise HTTPException(status_code=404, detail="Product not found")

	gallery = [product["image"]] + [
		item["image"] for item in all_products if item["id"] != product["id"]
	]
	similar_products = [
		{
			"id": item["id"],
			"name": item["name"],
			"image": item["image"],
			"price_range": f'${item["price"] - 8:.2f} - ${item["price"] + 12:.2f}',
		}
		for item in all_products
		if item["id"] != product["id"]
	][:4]

	return templates.TemplateResponse(
		request=request,
		name="product-details.html",
		context={
			"product": product,
			"gallery": gallery,
			"similar_products": similar_products,
		},
	)

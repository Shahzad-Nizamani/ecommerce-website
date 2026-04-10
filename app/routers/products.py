from math import ceil

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/views")

PRODUCTS = [
	{
		"id": 1,
		"name": "AeroFlex Running Shoes",
		"price": 79.99,
		"old_price": 96.25,
		"category": "Footwear",
		"image": "/assets/shoes.svg",
		"description": "Lightweight daily trainers built for comfort and speed.",
		"rating": 4.7,
		"reviews": 32,
		"orders": 154,
		"stock_label": "In stock",
		"material": "Breathable mesh and rubber",
		"design": "Performance-first silhouette for daily training",
		"sizes": ["40", "41", "42"],
		"seller_initial": "A",
		"supplier": "Aurora Athletics Ltd.",
		"location": "Germany, Berlin",
		"shipping": "Worldwide shipping",
		"price_tiers": [
			{"label": "50-100 pcs", "amount": 79.99, "accent": True},
			{"label": "100-700 pcs", "amount": 74.39, "accent": False},
			{"label": "700+ pcs", "amount": 67.99, "accent": False},
		],
		"specs": [
			{"label": "Model", "value": "# ARF-87991"},
			{"label": "Style", "value": "Athletic everyday"},
			{"label": "Certificate", "value": "ISO-8989"},
			{"label": "Size", "value": "EU 40-45"},
			{"label": "Memory", "value": "N/A"},
		],
		"features": [
			"Responsive sole for long walks and runs",
			"Quick-dry upper with soft inner padding",
			"Durable outsole built for everyday wear",
			"Easy returns and tracked delivery",
		],
	},
	{
		"id": 2,
		"name": "Nimbus Smart Watch",
		"price": 129.00,
		"old_price": 149.00,
		"category": "Wearables",
		"image": "/assets/watch.svg",
		"description": "Track fitness goals and notifications with all-day battery life.",
		"rating": 4.8,
		"reviews": 58,
		"orders": 236,
		"stock_label": "In stock",
		"material": "Aluminum frame and silicone strap",
		"design": "Minimal bezel with fitness-focused interface",
		"sizes": ["40mm", "44mm", "48mm"],
		"seller_initial": "N",
		"supplier": "Nimbus Devices Co.",
		"location": "Germany, Berlin",
		"shipping": "Worldwide shipping",
		"price_tiers": [
			{"label": "50-100 pcs", "amount": 129.00, "accent": True},
			{"label": "100-700 pcs", "amount": 119.97, "accent": False},
			{"label": "700+ pcs", "amount": 109.65, "accent": False},
		],
		"specs": [
			{"label": "Model", "value": "# NSW-11082"},
			{"label": "Style", "value": "Modern smart wearable"},
			{"label": "Certificate", "value": "CE / RoHS"},
			{"label": "Size", "value": "40mm to 48mm"},
			{"label": "Memory", "value": "32GB storage"},
		],
		"features": [
			"Heart-rate, sleep, and step tracking",
			"Long battery life with magnetic charging",
			"Notification sync for calls and apps",
			"Water-resistant build with premium finish",
		],
	},
	{
		"id": 3,
		"name": "Urban Sling Bag",
		"price": 49.50,
		"old_price": 61.40,
		"category": "Accessories",
		"image": "/assets/bag.svg",
		"description": "Compact carry bag with quick-access pockets and durable fabric.",
		"rating": 4.5,
		"reviews": 24,
		"orders": 118,
		"stock_label": "In stock",
		"material": "Water-resistant woven fabric",
		"design": "Compact commuter shape with multiple pockets",
		"sizes": ["Small", "Medium", "Large"],
		"seller_initial": "U",
		"supplier": "Urban Trail Supply",
		"location": "Germany, Berlin",
		"shipping": "Worldwide shipping",
		"price_tiers": [
			{"label": "50-100 pcs", "amount": 49.50, "accent": True},
			{"label": "100-700 pcs", "amount": 46.04, "accent": False},
			{"label": "700+ pcs", "amount": 42.07, "accent": False},
		],
		"specs": [
			{"label": "Model", "value": "# USB-50424"},
			{"label": "Style", "value": "Crossbody utility"},
			{"label": "Certificate", "value": "ISO-9001"},
			{"label": "Size", "value": "28cm x 16cm x 9cm"},
			{"label": "Memory", "value": "N/A"},
		],
		"features": [
			"Hidden zip pocket for valuables",
			"Adjustable strap for day-long comfort",
			"Lightweight build with structured base",
			"Easy-clean fabric for everyday carry",
		],
	},
	{
		"id": 4,
		"name": "Echo Wireless Earbuds",
		"price": 59.00,
		"old_price": 72.00,
		"category": "Audio",
		"image": "/assets/earbuds.svg",
		"description": "Crisp sound and noise isolation in a pocket-friendly case.",
		"rating": 4.6,
		"reviews": 41,
		"orders": 189,
		"stock_label": "In stock",
		"material": "Matte polymer shell",
		"design": "Compact charging case with secure-fit earbuds",
		"sizes": ["Standard", "Sport", "Pro"],
		"seller_initial": "E",
		"supplier": "Echo Audio Works",
		"location": "Germany, Berlin",
		"shipping": "Worldwide shipping",
		"price_tiers": [
			{"label": "50-100 pcs", "amount": 59.00, "accent": True},
			{"label": "100-700 pcs", "amount": 54.87, "accent": False},
			{"label": "700+ pcs", "amount": 50.15, "accent": False},
		],
		"specs": [
			{"label": "Model", "value": "# EWE-90310"},
			{"label": "Style", "value": "Wireless everyday audio"},
			{"label": "Certificate", "value": "FCC / CE"},
			{"label": "Size", "value": "Pocket charging case"},
			{"label": "Memory", "value": "Bluetooth 5.3 pairing"},
		],
		"features": [
			"Balanced sound with passive isolation",
			"Fast pairing and stable wireless connection",
			"Compact charging case with USB-C",
			"Comfortable fit for long listening sessions",
		],
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
	q = (request.query_params.get("q") or "").strip().lower()
	category = (request.query_params.get("category") or "").strip().lower()
	page = max(int(request.query_params.get("page") or 1), 1)
	page_size = 6

	filtered_products = [
		item
		for item in PRODUCTS
		if (
			(not q or q in item["name"].lower() or q in item["category"].lower())
			and (not category or item["category"].lower() == category)
		)
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
			"all_products": filtered_products,
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
	product = next((item for item in PRODUCTS if item["id"] == product_id), None)
	if product is None:
		raise HTTPException(status_code=404, detail="Product not found")

	gallery = [product["image"]] + [
		item["image"] for item in PRODUCTS if item["id"] != product["id"]
	]
	similar_products = [
		{
			"id": item["id"],
			"name": item["name"],
			"image": item["image"],
			"price_range": f'${item["price"] - 8:.2f} - ${item["price"] + 12:.2f}',
		}
		for item in PRODUCTS
		if item["id"] != product["id"]
	][:4]

	related_products = [
		{
			"id": item["id"],
			"name": item["name"],
			"image": item["image"],
			"price_range": f'${item["price"] - 6:.2f} - ${item["price"] + 10:.2f}',
		}
		for item in PRODUCTS
	]

	return templates.TemplateResponse(
		request=request,
		name="product-details.html",
		context={
			"product": product,
			"gallery": gallery,
			"similar_products": similar_products,
			"related_products": related_products,
		},
	)

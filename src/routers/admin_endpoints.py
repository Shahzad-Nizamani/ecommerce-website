from fastapi import APIRouter, Request, HTTPException, status, Form, Cookie, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from src.database.product_management import add_product
from src.database.user_queries import get_user_by_username
from src.utils.auth import SECRET_KEY, ALGORITHM
import os

router = APIRouter()
templates = Jinja2Templates(directory="src/views")


def get_current_user(access_token: str = Cookie(None)):
    """Get current user from token."""
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin", False)
        
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        
        return {"username": username, "is_admin": is_admin}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


def get_admin_user(user: dict = Depends(get_current_user)):
    """Get current admin user."""
    if not user["is_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


@router.get("/admin/products", response_class=HTMLResponse)
async def admin_products_page(request: Request, user: dict = Depends(get_admin_user)):
    """Render the admin products page."""
    return templates.TemplateResponse(
        request=request,
        name="admin-products.html",
        context={"username": user["username"]},
    )


@router.get("/admin/add-product", response_class=HTMLResponse)
async def add_product_page(request: Request, user: dict = Depends(get_admin_user)):
    """Render the add product page."""
    return templates.TemplateResponse(
        request=request,
        name="add-product.html",
        context={"username": user["username"]},
    )


@router.post("/admin/add-product")
async def create_product(
    request: Request,
    user: dict = Depends(get_admin_user),
    name: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    stock: int = Form(...),
    image: str = Form(None),
):
    """Handle product creation."""
    try:
        # Validation
        if not name or not category:
            return templates.TemplateResponse(
                request=request,
                name="add-product.html",
                context={
                    "error": "Product name and category are required",
                    "username": user["username"],
                },
            )
        
        if price <= 0:
            return templates.TemplateResponse(
                request=request,
                name="add-product.html",
                context={
                    "error": "Price must be greater than 0",
                    "username": user["username"],
                },
            )
        
        if stock < 0:
            return templates.TemplateResponse(
                request=request,
                name="add-product.html",
                context={
                    "error": "Stock cannot be negative",
                    "username": user["username"],
                },
            )
        
        # Add product to database
        result = add_product(
            name=name.strip(),
            price=float(price),
            category=category.strip(),
            description=description.strip() if description else "",
            stock=int(stock),
            image=image.strip() if image else None,
        )
        
        if not result["success"]:
            return templates.TemplateResponse(
                request=request,
                name="add-product.html",
                context={
                    "error": f"Failed to add product: {result.get('error', 'Unknown error')}",
                    "username": user["username"],
                },
            )
        
        # Redirect to products page with success message
        return templates.TemplateResponse(
            request=request,
            name="add-product.html",
            context={
                "success": f"Product '{name}' added successfully!",
                "username": user["username"],
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="add-product.html",
            context={
                "error": f"Error adding product: {str(e)}",
                "username": user["username"],
            },
        )


# API endpoint for adding products
@router.post("/api/admin/products")
async def api_create_product(
    user: dict = Depends(get_admin_user),
    name: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    stock: int = Form(...),
    image: str = Form(None),
):
    """API endpoint for creating products."""
    if not name or not category:
        raise HTTPException(status_code=400, detail="Name and category are required")
    
    if price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")
    
    if stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")
    
    result = add_product(
        name=name.strip(),
        price=float(price),
        category=category.strip(),
        description=description.strip() if description else "",
        stock=int(stock),
        image=image.strip() if image else None,
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to add product"))
    
    return result

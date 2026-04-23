from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from src.database.user_queries import create_user, verify_user_credentials
from src.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()
templates = Jinja2Templates(directory="src/views")


class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.get("/auth/signup", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    """Render the signup page."""
    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={},
    )


@router.post("/auth/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
):
    """Handle user signup."""
    try:
        username = username.strip()
        email = email.strip()
        password = password.strip()
        password_confirm = password_confirm.strip()
        
        # Validation
        if not username or not email or not password:
            return templates.TemplateResponse(
                request=request,
                name="signup.html",
                context={"error": "All fields are required"},
            )
        
        if len(password) < 6:
            return templates.TemplateResponse(
                request=request,
                name="signup.html",
                context={"error": "Password must be at least 6 characters"},
            )
        
        if password != password_confirm:
            return templates.TemplateResponse(
                request=request,
                name="signup.html",
                context={"error": "Passwords do not match"},
            )
        
        # Create user
        result = create_user(username, email, password)
        
        if not result["success"]:
            return templates.TemplateResponse(
                request=request,
                name="signup.html",
                context={"error": result.get("error", "Signup failed")},
            )
        
        # Redirect to login with success message
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"success": "Account created successfully! Please login."},
        )
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context={"error": f"Signup failed: {str(e)}"},
        )


@router.get("/auth/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    """Render the login page."""
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )


@router.post("/auth/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    """Handle user login."""
    try:
        username = username.strip()
        password = password.strip()
        
        # Validation
        if not username or not password:
            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={"error": "Username and password are required"},
            )
        
        # Verify credentials
        result = verify_user_credentials(username, password)
        
        if not result["success"]:
            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={"error": "Invalid username or password"},
            )
        
        user = result["user"]
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["username"], "is_admin": user["is_admin"]},
            expires_delta=access_token_expires,
        )
        
        # Redirect to products page with token in cookie
        response = RedirectResponse(url="/products", status_code=302)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return response
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": f"Login failed: {str(e)}"},
        )


@router.get("/auth/logout")
def logout(request: Request):
    """Handle user logout."""
    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response


# API endpoints for authentication (for client-side usage)
@router.post("/api/auth/signup")
async def api_signup(data: SignupRequest):
    """API endpoint for signup."""
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    if data.password != data.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    result = create_user(data.username, data.email, data.password)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Signup failed"))
    
    return {"success": True, "message": "User created successfully"}


@router.post("/api/auth/login")
async def api_login(data: LoginRequest):
    """API endpoint for login."""
    result = verify_user_credentials(data.username, data.password)
    
    if not result["success"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = result["user"]
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "is_admin": user["is_admin"]},
        expires_delta=access_token_expires,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user["username"],
        "is_admin": user["is_admin"],
    }

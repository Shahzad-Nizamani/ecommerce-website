import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.routers import home_endpoints, product_endpoints

app = FastAPI(title="Ecommerce Backend")

cors_origins_env = os.getenv("CORS_ORIGINS", "")
allowed_origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]

if not allowed_origins:
	allowed_origins = [
		"http://localhost:3000",
		"http://localhost:5173",
		"https://localhost:5173",
	]

app.add_middleware(
	CORSMiddleware,
	allow_origins=allowed_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="src/public"), name="public")
app.mount("/assets", StaticFiles(directory="src/assets"), name="assets")


@app.get("/")
def root():
	return RedirectResponse(url="/products")


app.include_router(home_endpoints.router)
app.include_router(product_endpoints.router)
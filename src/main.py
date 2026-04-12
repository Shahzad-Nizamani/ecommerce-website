from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.routers import home_endpoints, product_endpoints

app = FastAPI(title="Ecommerce Backend")

app.mount("/public", StaticFiles(directory="src/public"), name="public")
app.mount("/assets", StaticFiles(directory="src/assets"), name="assets")


@app.get("/")
def root():
	return RedirectResponse(url="/products")


app.include_router(home_endpoints.router)
app.include_router(product_endpoints.router)
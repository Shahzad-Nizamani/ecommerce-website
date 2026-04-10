from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import products


app = FastAPI(title="Ecommerce Backend")

app.mount("/public", StaticFiles(directory="app/public"), name="public")
app.mount("/assets", StaticFiles(directory="app/assets"), name="assets")

app.include_router(products.router)
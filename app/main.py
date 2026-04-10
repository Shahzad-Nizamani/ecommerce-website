from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.products import router as web_router

app = FastAPI(title="Ecommerce Backend Design")

app.mount("/public", StaticFiles(directory="app/public"), name="public")
app.mount("/assets", StaticFiles(directory="app/assets"), name="assets")

app.include_router(web_router)

from fastapi import FastAPI
from src.api.v1 import auth, ingredients, orders

app = FastAPI(title="O-Platy-60")

app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(orders.router)

from fastapi import FastAPI
from src.api.v1 import auth


app = FastAPI(title="O-Platy-60")

app.include_router(auth.router)

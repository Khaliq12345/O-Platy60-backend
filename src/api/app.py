import os
import sys

# Ajoute la racine du projet au PYTHONPATH si besoin
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


from fastapi import FastAPI
from src.api.v1 import auth
from src.api.v1 import ingredients

app = FastAPI(title="O-Platy-60")

app.include_router(auth.router)
app.include_router(ingredients.router)

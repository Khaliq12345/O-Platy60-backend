from fastapi import APIRouter
from src.schemas import auth_schema

router = APIRouter(prefix="/v1/auth", tags=["AUTH"])


@router.get("/login")
def login(email: str, password: str) -> auth_schema.Login:
    return auth_schema.Login(email=email, password=password)

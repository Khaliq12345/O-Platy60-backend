from fastapi import APIRouter
from src.schemas import auth_schema

router = APIRouter(prefix="/v1/auth", tags=["AUTH"])


@router.post("/login")
def login(credentials: auth_schema.Login) -> auth_schema.Login:
    return auth_schema.Login(
        email=credentials.email, password=credentials.password
    )

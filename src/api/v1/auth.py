from fastapi import APIRouter, HTTPException, Depends
from src.schemas import auth_schema
from src.services.supabase_service import SupabaseService
from gotrue.errors import AuthApiError

router = APIRouter(prefix="/api/auth", tags=["AUTH"])

# Dependency to get the Supabase service
def get_supabase_service():
    return SupabaseService()

@router.post("/login", response_model=auth_schema.Session)
def login(credentials: auth_schema.Login, db: SupabaseService = Depends(get_supabase_service)):
    """Signs in a user."""
    try:
        response = db.client.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return response.session
    except AuthApiError as e:
        raise HTTPException(status_code=e.status, detail=e.message)

@router.post("/refresh", response_model=auth_schema.Session)
def refresh(refresh_data: auth_schema.Refresh, db: SupabaseService = Depends(get_supabase_service)):
    """Refreshes a user session."""
    try:
        response = db.client.auth.refresh_session(refresh_data.refresh_token)
        return response.session
    except AuthApiError as e:
        raise HTTPException(status_code=e.status, detail=e.message)

@router.post("/logout")
def logout(token: auth_schema.Token, db: SupabaseService = Depends(get_supabase_service)):
    """Signs out a user."""
    try:
        db.client.auth.set_session(token.access_token, token.refresh_token)
        db.client.auth.sign_out()
        return {"detail": "User logged out"}
    except AuthApiError as e:
        raise HTTPException(status_code=e.status, detail=e.message)

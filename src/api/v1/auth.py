from fastapi import APIRouter, Depends
from src.schemas import auth_schema
from src.services.supabase_service import SupabaseService

router = APIRouter(prefix="/api/v1/auth", tags=["AUTH"])

# Dependency to get the Supabase service
def get_supabase_service():
    return SupabaseService()

@router.post("/login", response_model=auth_schema.Session)
def login(credentials: auth_schema.Login, supabase: SupabaseService = Depends(get_supabase_service)):
    """Signs in a user."""
    return supabase.login(credentials)

@router.post("/refresh", response_model=auth_schema.Session)
def refresh(refresh_data: auth_schema.Refresh, supabase: SupabaseService = Depends(get_supabase_service)):
    """Refreshes a user session."""
    return supabase.refresh_session(refresh_data)

@router.post("/logout")
def logout(token: auth_schema.Token, supabase: SupabaseService = Depends(get_supabase_service)):
    """Signs out a user."""
    return supabase.logout(token)

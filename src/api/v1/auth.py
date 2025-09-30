from fastapi import APIRouter, Depends, HTTPException
from supabase import AuthInvalidCredentialsError
from src.schemas import auth_schema
from src.services.supabase_service import SupabaseService

router = APIRouter(prefix="/api/v1/auth", tags=["AUTH"])


# Dependency to get the Supabase service
def get_supabase_service():
    return SupabaseService()


@router.post("/login", response_model=auth_schema.Session)
def login(
    credentials: auth_schema.Login,
    supabase: SupabaseService = Depends(get_supabase_service),
):
    """Signs in a user."""
    try:
        return supabase.login(credentials)
    except AuthInvalidCredentialsError as e:
        raise HTTPException(status_code=400, detail=f"Invalid credentials - {e}")
    except Exception as e:
        raise HTTPException(status_code=505, detail=f"Server Error - {e}")


@router.post("/refresh", response_model=auth_schema.Session)
def refresh(
    refresh_data: auth_schema.Refresh,
    supabase: SupabaseService = Depends(get_supabase_service),
):
    """Refreshes a user session."""
    try:
        return supabase.refresh_session(refresh_data)
    except AuthInvalidCredentialsError as e:
        raise HTTPException(status_code=400, detail=f"Invalid credentials - {e}")
    except Exception as e:
        raise HTTPException(status_code=505, detail=f"Server Error - {e}")


@router.post("/logout")
def logout(
    token: auth_schema.Token, supabase: SupabaseService = Depends(get_supabase_service)
):
    """Signs out a user."""
    try:
        return supabase.logout(token)
    except AuthInvalidCredentialsError as e:
        raise HTTPException(status_code=400, detail=f"Invalid credentials - {e}")
    except Exception as e:
        raise HTTPException(status_code=505, detail=f"Server Error - {e}")

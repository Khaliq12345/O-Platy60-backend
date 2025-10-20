from fastapi import APIRouter, HTTPException
from supabase import AuthInvalidCredentialsError
from src.schemas import auth_schema
from src.services.supabase_services.supabase_service import SupabaseService
from src.api.dependencies import supabase_depends

router = APIRouter(prefix="/api/v1/auth", tags=["AUTH"])


@router.post("/login", response_model=auth_schema.Session)
def login(
    credentials: auth_schema.Login,
    supabase: SupabaseService = supabase_depends,
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
    token: auth_schema.Token,
    supabase: SupabaseService = supabase_depends,
):
    """Refreshes a user session."""
    try:
        return supabase.refresh_session(token)
    except AuthInvalidCredentialsError as e:
        raise HTTPException(status_code=400, detail=f"Invalid credentials - {e}")
    except Exception as e:
        raise HTTPException(status_code=505, detail=f"Server Error - {e}")


@router.post("/logout")
def logout(token: auth_schema.Token, supabase: SupabaseService = supabase_depends):
    """Signs out a user."""
    try:
        return supabase.logout(token)
    except AuthInvalidCredentialsError as e:
        raise HTTPException(status_code=400, detail=f"Invalid credentials - {e}")
    except Exception as e:
        raise HTTPException(status_code=505, detail=f"Server Error - {e}")

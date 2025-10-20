from fastapi import APIRouter, HTTPException
from supabase import AuthInvalidCredentialsError
from src.schemas import auth_schema
from src.services.supabase_services.supabase_service import SupabaseService
from src.api.dependencies import supabase_depends

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])

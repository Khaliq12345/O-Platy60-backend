from fastapi import Depends
from src.services.supabase_services.supabase_service import SupabaseService


# Dependency to get the Supabase service
def get_supabase_service():
    return SupabaseService()


supabase_depends = Depends(get_supabase_service)

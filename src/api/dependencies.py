from fastapi import Depends
from src.services.supabase_services.supabase_service import SupabaseService
from src.services.supabase_services.order_service import OrdersService


# Dependency to get the Supabase service
def get_supabase_service():
    return SupabaseService()


# Dependency to get the Orders service
def get_orders_service():
    return OrdersService()


supabase_depends = Depends(get_supabase_service)
orders_depends = Depends(get_orders_service)

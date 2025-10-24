from fastapi import Depends
from src.services.supabase_services.supabase_service import SupabaseService
from src.services.supabase_services.order_service import OrdersService
from src.services.supabase_services.ingredient_service import IngredientService
from src.services.supabase_services.recipe_service import RecipeService


# Dependency to get the Supabase service
def get_supabase_service():
    return SupabaseService()


supabase_depends = Depends(get_supabase_service)

order_depends = Depends(OrdersService)
ingredient_depends = Depends(IngredientService)
recipe_depends = Depends(RecipeService)

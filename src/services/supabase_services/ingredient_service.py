from src.services.supabase_services.supabase_service import SupabaseService


class IngredientService(SupabaseService):
    def __init__(self) -> None:
        super().__init__()

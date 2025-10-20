from src.services.supabase_services.supabase_service import SupabaseService


class OrderService(SupabaseService):
    def __init__(self) -> None:
        super().__init__()

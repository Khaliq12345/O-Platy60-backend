from supabase import Client, create_client
from src.core.config import Config


class SupabaseService:
    def __init__(self) -> None:
        self.config = Config()
        self.client: Client = create_client(
            self.config.SUPABASE_URL, self.config.SUPABASE_KEY
        )

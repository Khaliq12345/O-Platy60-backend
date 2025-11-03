import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self) -> None:
        self.SUPABASE_URL = os.getenv("SUPABASE_URL", "")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
        self.SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "")

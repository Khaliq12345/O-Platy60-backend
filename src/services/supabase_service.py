from supabase import (
    Client,
    create_client,
)
from src.core.config import Config
from src.schemas import auth_schema


class SupabaseService:
    def __init__(self) -> None:
        self.config = Config()
        self.client: Client = create_client(
            self.config.SUPABASE_URL, self.config.SUPABASE_KEY
        )

    def login(self, credentials: auth_schema.Login):
        """Login a user"""
        response = self.client.auth.sign_in_with_password(
            {"email": credentials.email, "password": credentials.password}
        )
        return response.session

    def refresh_session(self, refresh_data: auth_schema.Token):
        """Refresh a user session"""
        self.client.auth.set_session(
            refresh_data.access_token, refresh_data.refresh_token
        )
        response = self.client.auth.refresh_session()
        return response.session

    def logout(self, token: auth_schema.Token):
        """Logout a user"""
        self.client.auth.set_session(token.access_token, token.refresh_token)
        self.client.auth.sign_out()
        return {"detail": "User logged out"}

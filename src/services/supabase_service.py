from supabase import Client, create_client
from src.core.config import Config
from src.schemas import auth_schema
from gotrue.errors import AuthApiError
from fastapi import HTTPException


class SupabaseService:
    def __init__(self) -> None:
        self.config = Config()
        self.client: Client = create_client(
            self.config.SUPABASE_URL, self.config.SUPABASE_KEY
        )

    def login(self, credentials: auth_schema.Login):
        try:
            response = self.client.auth.sign_in_with_password(
                {"email": credentials.email, "password": credentials.password}
            )
            return response.session
        except AuthApiError as e:
            raise HTTPException(status_code=e.status, detail=e.message)

    def refresh_session(self, refresh_data: auth_schema.Refresh):
        try:
            response = self.client.auth.refresh_session(refresh_data.refresh_token)
            return response.session
        except AuthApiError as e:
            raise HTTPException(status_code=e.status, detail=e.message)

    def logout(self, token: auth_schema.Token):
        try:
            self.client.auth.set_session(token.access_token, token.refresh_token)
            self.client.auth.sign_out()
            return {"detail": "User logged out"}
        except AuthApiError as e:
            raise HTTPException(status_code=e.status, detail=e.message)

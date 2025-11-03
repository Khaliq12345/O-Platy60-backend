from src.services.supabase_services.supabase_service import SupabaseService


class StorageService(SupabaseService):
    def __init__(self) -> None:
        super().__init__()
        self.bucket = self.config.SUPABASE_STORAGE_BUCKET

    def upload_file(
        self,
        file_content: bytes,
        file_id: str,
        file_format: str,
        folder: str,
    ) -> str:
        if not self.bucket:
            raise ValueError("Supabase storage bucket is not configured.")
        if not file_content:
            raise ValueError("File content is empty.")
        if not file_id:
            raise ValueError("File identifier is required.")

        extension = file_format.lstrip(".")
        filename = f"{file_id}.{extension}" if extension else file_id
        safe_folder = folder.strip().strip("/\\")
        path_parts = [segment for segment in [safe_folder, filename] if segment]
        storage_path = "/".join(path_parts) or filename

        upload_response = self.client.storage.from_(self.bucket).upload(
            path=storage_path,
            file=file_content,
        )
        error = getattr(upload_response, "error", None)
        if error:
            message = getattr(error, "message", "Upload failed.")
            raise ValueError(message)
        if isinstance(upload_response, dict):
            error_payload = upload_response.get("error")
            if error_payload:
                message = error_payload.get("message", "Upload failed.")
                raise ValueError(message)

        public_url_response = self.client.storage.from_(self.bucket).get_public_url(
            path=storage_path
        )
        error = getattr(public_url_response, "error", None)
        if error:
            message = getattr(error, "message", "Failed to get public URL.")
            raise ValueError(message)

        data = getattr(public_url_response, "data", None)
        if isinstance(data, dict):
            public_url = data.get("publicUrl")
            if public_url:
                return public_url
        if isinstance(public_url_response, dict):
            data = public_url_response.get("data") or {}
            public_url = data.get("publicUrl")
            if public_url:
                return public_url

        base_url = self.config.SUPABASE_URL.rstrip("/")
        if base_url:
            return f"{base_url}/storage/v1/object/public/{self.bucket}/{storage_path}"

        raise ValueError("Unable to retrieve public URL after upload.")

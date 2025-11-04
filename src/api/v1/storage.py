from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from src.api.dependencies import storage_depends
from src.services.supabase_services.storage_service import StorageService

router = APIRouter(prefix="/api/v1/storage", tags=["Storage"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_to_storage(
    file: UploadFile = File(...),
    file_id: str = Form(...),
    file_format: str = Form(...),
    folder: str = Form(...),
    storage_service: StorageService = storage_depends,
) -> dict[str, str]:
    try:
        file_bytes = await file.read()
        public_url = storage_service.upload_file(
            file_bytes, file_id, file_format, folder
        )
        return {"public_url": public_url}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file - {exc}",
        )

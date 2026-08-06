from fastapi import APIRouter, File, UploadFile

from app.schemas.upload import UploadResponse
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)

document_service = DocumentService()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    result = await document_service.save_upload(file)

    return UploadResponse(
        success=True,
        message="Document uploaded successfully.",
        **result,
    )
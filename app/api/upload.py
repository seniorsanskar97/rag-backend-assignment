from pathlib import Path

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

    extracted_text = document_service.extract_text(
        Path(result["file_path"])
    )

    print(f"Extracted {len(extracted_text)} characters")

    return UploadResponse(
        success=True,
        document_id=result["document_id"],
        filename=result["filename"],
        content_type=result["content_type"],
        size_bytes=result["size_bytes"],
        message=f"Document uploaded successfully. Extracted {len(extracted_text)} characters.",
    )
from pathlib import Path

from fastapi import APIRouter, File, Query, UploadFile

from app.schemas.upload import UploadResponse
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)

document_service = DocumentService()
chunking_service = ChunkingService()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    strategy: str = Query("fixed", enum=["fixed", "paragraph"]),
):
    result = await document_service.save_upload(file)

    extracted_text = document_service.extract_text(
        Path(result["file_path"])
    )

    if strategy == "paragraph":
        chunks = chunking_service.paragraph_chunking(extracted_text)
    else:
        chunks = chunking_service.fixed_size_chunking(extracted_text)

    print(f"Created {len(chunks)} chunks")

    return UploadResponse(
        success=True,
        document_id=result["document_id"],
        filename=result["filename"],
        content_type=result["content_type"],
        size_bytes=result["size_bytes"],
        message=f"Document uploaded successfully. Created {len(chunks)} chunks.",
    )
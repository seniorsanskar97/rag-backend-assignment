from pathlib import Path

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.upload import UploadResponse
from app.services.chunking_service import ChunkingService
from app.services.database_service import DatabaseService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import qdrant_service

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)

document_service = DocumentService()
chunking_service = ChunkingService()
database_service = DatabaseService()
embedding_service = EmbeddingService()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    strategy: str = Query("fixed", enum=["fixed", "paragraph"]),
    db: Session = Depends(get_db),
):
    result = await document_service.save_upload(file)

    extracted_text = document_service.extract_text(
        Path(result["file_path"])
    )

    if strategy == "paragraph":
        chunks = chunking_service.paragraph_chunking(extracted_text)
    else:
        chunks = chunking_service.fixed_size_chunking(extracted_text)

    database_service.save_document(
        db=db,
        document_data=result,
    )

    embeddings = [
        embedding_service.generate_embedding(chunk)
        for chunk in chunks
    ]

    qdrant_service.store_chunks(
        document_id=result["document_id"],
        chunks=chunks,
        embeddings=embeddings,
    )

    return UploadResponse(
        success=True,
        document_id=result["document_id"],
        filename=result["filename"],
        content_type=result["content_type"],
        size_bytes=result["size_bytes"],
        message=f"Uploaded successfully. Created {len(chunks)} chunks.",
    )
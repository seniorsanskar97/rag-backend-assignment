from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile


class DocumentService:
    ALLOWED_EXTENSIONS = {".pdf", ".txt"}

    def __init__(self):
        self.upload_dir = Path("app/uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, file: UploadFile) -> dict:
        extension = Path(file.filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and TXT files are supported."
            )

        document_id = str(uuid4())
        stored_filename = f"{document_id}{extension}"
        file_path = self.upload_dir / stored_filename

        content = await file.read()

        with open(file_path, "wb") as output_file:
            output_file.write(content)

        return {
            "document_id": document_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(content),
        }
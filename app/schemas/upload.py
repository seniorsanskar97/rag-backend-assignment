from pydantic import BaseModel


class UploadResponse(BaseModel):
    success: bool
    document_id: str
    filename: str
    content_type: str
    size_bytes: int
    message: str
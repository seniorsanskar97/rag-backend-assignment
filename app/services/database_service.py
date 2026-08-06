from sqlalchemy.orm import Session

from app.models.document import Document


class DatabaseService:

    def save_document(
        self,
        db: Session,
        document_data: dict,
    ) -> Document:

        document = Document(
            document_id=document_data["document_id"],
            filename=document_data["filename"],
            content_type=document_data["content_type"],
            size_bytes=document_data["size_bytes"],
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document
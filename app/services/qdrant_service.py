from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import QDRANT_COLLECTION, QDRANT_URL


class QdrantService:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL)

        collections = self.client.get_collections().collections

        if not any(c.name == QDRANT_COLLECTION for c in collections):
            self.client.create_collection(
                collection_name=QDRANT_COLLECTION,
                vectors_config=VectorParams(
                    size=3072,
                    distance=Distance.COSINE,
                ),
            )

    def store_chunks(
        self,
        document_id: str,
        chunks: list[str],
        embeddings: list[list[float]],
    ):
        points = []

        for chunk, embedding in zip(chunks, embeddings):
            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "document_id": document_id,
                        "text": chunk,
                    },
                )
            )

        self.client.upsert(
            collection_name=QDRANT_COLLECTION,
            points=points,
        )


qdrant_service = QdrantService()
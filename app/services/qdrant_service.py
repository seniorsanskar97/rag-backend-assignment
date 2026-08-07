from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

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


qdrant_service = QdrantService()
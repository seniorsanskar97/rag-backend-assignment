from app.services.embedding_service import EmbeddingService

service = EmbeddingService()

embedding = service.generate_embedding("Hello Palm Mind AI")

print(len(embedding))
from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import llm_service
from app.services.qdrant_service import qdrant_service

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)

embedding_service = EmbeddingService()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    embedding = embedding_service.generate_embedding(
        request.question
    )

    chunks = qdrant_service.search(embedding)

    answer = llm_service.generate_answer(
        request.question,
        chunks,
    )

    return ChatResponse(
        answer=answer,
        retrieved_chunks=chunks,
    )
from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_memory_service import chat_memory_service
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
    # Get previous conversation from Redis
    history = chat_memory_service.get_history(request.session_id)

    embedding = embedding_service.generate_embedding(
        request.question
    )

    chunks = qdrant_service.search(embedding)

    history_text = "\n".join(history)

    full_question = f"""
Previous conversation:
{history_text}

Current question:
{request.question}
"""

    answer = llm_service.generate_answer(
        full_question,
        chunks,
    )

    chat_memory_service.add_message(
        request.session_id,
        "User",
        request.question,
    )

    chat_memory_service.add_message(
        request.session_id,
        "Assistant",
        answer,
    )

    return ChatResponse(
        answer=answer,
        retrieved_chunks=chunks,
    )
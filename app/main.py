from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.upload import router as upload_router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Palm Mind AI Assignment",
    version="1.0.0",
    description="Backend for document ingestion and conversational RAG.",
)

app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "Palm Mind AI Backend is running!"}
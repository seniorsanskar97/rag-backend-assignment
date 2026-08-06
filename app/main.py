from fastapi import FastAPI

from app.api.upload import router as upload_router

app = FastAPI(
    title="Palm Mind AI Assignment",
    version="1.0.0",
    description="Backend for document ingestion and conversational RAG.",
)

app.include_router(upload_router)


@app.get("/")
def root():
    return {"message": "Palm Mind AI Backend is running!"}
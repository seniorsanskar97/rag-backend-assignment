from fastapi import FastAPI

app = FastAPI(
    title="Palm Mind AI Assignment",
    version="1.0.0",
    description="Backend for document ingestion and conversational RAG."
)


@app.get("/")
def root():
    return {
        "message": "Palm Mind AI Backend is running!"
    }
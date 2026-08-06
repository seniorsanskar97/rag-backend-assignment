from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document():
    return {
        "success": True,
        "message": "Upload endpoint is ready."
    }
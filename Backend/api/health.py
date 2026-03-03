"""
Health check and welcome endpoints.
"""

from fastapi import APIRouter

from models.schemas import HealthResponse

router = APIRouter()


@router.get("/welcome")
async def welcome():
    """Welcome endpoint."""
    return {"answer": "Hi! 👋 How may I help you?", "source_chunks": ["Jindal Assistant"]}


@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    # Import here to avoid circular imports
    import api.chat
    vector_store = getattr(api.chat, 'vector_store', None)
    chunks_db = getattr(api.chat, 'chunks_db', [])
    
    return {
        "status": "ok",
        "vector_store_ready": vector_store is not None,
        "chunks_loaded": len(chunks_db)
    }

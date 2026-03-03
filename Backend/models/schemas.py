"""
Pydantic models and data schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID


class KnowledgeChunk(BaseModel):
    """Represents a chunk of knowledge extracted from a document."""
    content: str
    source_type: str  # pdf, excel, csv, pptx
    source_name: str
    source_path: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    structure: Dict[str, Any] = Field(default_factory=dict)


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str
    source_chunks: List[str] = Field(default_factory=list)
    session_id: str


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    vector_store_ready: bool
    chunks_loaded: int

"""
Jindal Operations Assistant - FastAPI Main Application
Clean architecture with separated concerns.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from config import DATA_DIR, INDEX_DIR, EMBEDDINGS_FILE, CHUNKS_FILE, LLM_MODEL, LLM_OPTIONS, MAX_CONCURRENT_LLM_CALLS, CORS_ORIGINS, HOST, PORT
from ingestion.loader import ingest_documents
from vectorstore.faiss_index import build_faiss_index, load_index, save_index
from api.chat import router as chat_router
from api.health import router as health_router

# Global shared state
vector_store = None
chunks_db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize vector store and shared state on app startup."""
    global vector_store, chunks_db
    
    print("Initializing RAG system...")
    
    # Check if index already exists
    import os
    if (os.path.exists(INDEX_DIR) and 
        os.path.exists(EMBEDDINGS_FILE) and 
        os.path.exists(CHUNKS_FILE)):
        try:
            print("Loading existing FAISS index...")
            embeddings_array, chunks_db = load_index(INDEX_DIR, EMBEDDINGS_FILE, CHUNKS_FILE)
            if embeddings_array is not None and chunks_db:
                import faiss
                dimension = embeddings_array.shape[1]
                vector_store = faiss.IndexFlatL2(dimension)
                vector_store.add(embeddings_array)
                print(f"Loaded {len(chunks_db)} chunks from cache.")
            else:
                print("Failed to load index, rebuilding...")
                raise Exception("Invalid cache")
        except Exception as e:
            print(f"Error loading index: {e}")
            print("Building new FAISS index...")
            chunks_db = ingest_documents(DATA_DIR)
            vector_store, embeddings_array = build_faiss_index(chunks_db)
            if vector_store and embeddings_array is not None:
                save_index(embeddings_array, chunks_db, INDEX_DIR, EMBEDDINGS_FILE, CHUNKS_FILE)
    else:
        print("Building new FAISS index...")
        chunks_db = ingest_documents(DATA_DIR)
        vector_store, embeddings_array = build_faiss_index(chunks_db)
        if vector_store and embeddings_array is not None:
            save_index(embeddings_array, chunks_db, INDEX_DIR, EMBEDDINGS_FILE, CHUNKS_FILE)
    
    # Update global state in chat module
    import api.chat
    api.chat.vector_store = vector_store
    api.chat.chunks_db = chunks_db
    
    print("RAG system ready!")
    
    yield
    
    # Cleanup (if needed)
    print("Shutting down RAG system...")


# Create FastAPI app
app = FastAPI(
    title="Jindal Operations Assistant",
    description="RAG-powered assistant for Jindal Power policies and procedures",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS != [""] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(health_router, prefix="/api", tags=["health"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Jindal Operations Assistant API", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)

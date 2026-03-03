"""
FAISS index management.
Handles building, loading, and saving FAISS indices.
"""

import os
import pickle
import numpy as np
import faiss
from typing import List, Tuple, Optional

from models.schemas import KnowledgeChunk
from .embeddings import generate_batch_embeddings


def build_faiss_index(chunks: List[KnowledgeChunk], embed_model: str = "mxbai-embed-large") -> Tuple[Optional[faiss.IndexFlatL2], Optional[np.ndarray]]:
    """
    Generate embeddings from KnowledgeChunk content and build FAISS index.
    Returns the FAISS index and embeddings array.
    """
    if not chunks:
        return None, None

    # Generate embeddings
    texts = [c.content for c in chunks]
    embeddings_array = generate_batch_embeddings(texts, model=embed_model)
    
    if embeddings_array.size == 0:
        return None, None

    # Build FAISS index
    dimension = embeddings_array.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_array)

    print(f"FAISS index built with {index.ntotal} vectors")

    return index, embeddings_array


def save_index(embeddings_array: np.ndarray, chunks: List[KnowledgeChunk], index_dir: str, embeddings_file: str, chunks_file: str):
    """Save embeddings and chunks to disk."""
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
    
    with open(embeddings_file, "wb") as f:
        pickle.dump(embeddings_array, f)
    
    with open(chunks_file, "wb") as f:
        pickle.dump(chunks, f)
    
    print("FAISS index and chunks saved.")


def load_index(index_dir: str, embeddings_file: str, chunks_file: str) -> Tuple[Optional[np.ndarray], Optional[List[KnowledgeChunk]]]:
    """Load embeddings and chunks from disk."""
    try:
        with open(chunks_file, "rb") as f:
            chunks = pickle.load(f)
        
        with open(embeddings_file, "rb") as f:
            embeddings_array = pickle.load(f)
        
        print(f"Loaded {len(chunks)} chunks and embeddings from disk.")
        return embeddings_array, chunks
    except Exception as e:
        print(f"Error loading index: {e}")
        return None, None

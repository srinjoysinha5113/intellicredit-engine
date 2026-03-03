"""
Embedding generation using Ollama.
"""

from config import EMBED_MODEL
import ollama
import numpy as np
from typing import List


def get_query_embedding(query: str, model: str = None) -> np.ndarray:
    """Generate embedding for a single query."""
    if model is None:
        model = EMBED_MODEL
    try:
        response = ollama.embed(model=model, input=[query])
        return np.array(response["embeddings"][0]).astype("float32")
    except Exception as e:
        print(f"Error generating query embedding: {e}")
        # Return zero embedding as fallback
        return np.zeros(1024, dtype="float32")


def generate_batch_embeddings(texts: List[str], model: str = None, batch_size: int = 1) -> np.ndarray:
    """
    Generate embeddings for a list of texts in batches.
    Handles context length limits and provides fallbacks.
    """
    if model is None:
        model = EMBED_MODEL
    all_embeddings = []
    
    print(f"Generating embeddings for {len(texts)} chunks in batches of {batch_size}...")

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        try:
            response = ollama.embed(model=model, input=batch_texts)
            batch_embeddings = np.array(response["embeddings"]).astype("float32")
            all_embeddings.append(batch_embeddings)
            print(f"Embedded batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
        except Exception as e:
            print(f"Error embedding batch {i//batch_size + 1}: {e}")
            # Fallback: embed one by one for this batch
            for text in batch_texts:
                try:
                    response = ollama.embed(model=model, input=[text])
                    single_embedding = np.array(response["embeddings"]).astype("float32")
                    all_embeddings.append(single_embedding)
                except Exception as e2:
                    print(f"Failed to embed single text: {e2}")
                    # Add zero embedding as last resort
                    zero_emb = np.zeros((1, 1024), dtype="float32")
                    all_embeddings.append(zero_emb)

    if not all_embeddings:
        print("No embeddings generated successfully")
        return np.array([])

    return np.vstack(all_embeddings)

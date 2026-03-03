"""
Main retrieval logic with FAISS search and ranking.
"""

import numpy as np
import faiss
from typing import List, Dict, Any

from config import CHUNK_MIN_WORDS
from models.schemas import KnowledgeChunk
from vectorstore.embeddings import get_query_embedding
from retrieval.preprocess import preprocess_query, expand_query


def retrieve_relevant_chunks(query: str, vector_store: faiss.IndexFlatL2, chunks_db: List[KnowledgeChunk], k: int = 8) -> List[str]:
    """
    Enhanced retrieval with query expansion and smart filtering.
    """
    # Preprocess query
    processed_query = preprocess_query(query)
    
    # Get query embedding
    query_embedding = get_query_embedding(processed_query)
    query_embedding = query_embedding.reshape(1, -1)
    
    # Search with higher recall (2x k)
    distances, indices = vector_store.search(query_embedding, k * 2)
    
    # Collect all results
    all_results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(chunks_db):
            chunk = chunks_db[idx]
            # Convert distance to similarity score (lower distance = higher similarity)
            score = 1 / (1 + dist)
            all_results.append({
                'chunk': chunk,
                'score': score,
                'distance': dist
            })
    
    # Remove duplicates and sort by score
    unique_results = {}
    for result in all_results:
        chunk_id = id(result['chunk'])
        if chunk_id not in unique_results or result['score'] > unique_results[chunk_id]['score']:
            unique_results[chunk_id] = result
    
    # Sort by relevance score and get top results
    sorted_results = sorted(unique_results.values(), key=lambda x: x['score'], reverse=True)
    
    # If query asks about "covered under", prioritize policy documents
    if "covered under" in query.lower():
        policy_results = [r for r in sorted_results if 'policy' in r['chunk'].metadata.get('category', '').lower()]
        if policy_results:
            sorted_results = policy_results
    
    # Format output
    retrieved = []
    for result in sorted_results[:k]:
        chunk = result['chunk']
        chunk_text = chunk.content
        source = chunk.source_name
        page = chunk.structure.get("page", "Unknown")
        category = chunk.metadata.get("category", "General")
        subcategory = chunk.metadata.get("subcategory")
        
        # Filter out very short chunks
        if len(chunk_text.split()) < CHUNK_MIN_WORDS:
            continue
            
        citation = f"[Source: {source}, Page {page}, Category: {category}"
        if subcategory:
            citation += f", Subcategory: {subcategory}"
        citation += f", Score: {result['score']:.3f}]"
        retrieved.append(f"{chunk_text}\n{citation}")

    return retrieved

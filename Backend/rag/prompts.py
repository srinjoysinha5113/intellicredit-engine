"""
Prompt builders for different RAG modes.
"""

from typing import List


def build_rag_prompt(query: str, retrieved_chunks: List[str]) -> str:
    """
    Build RAG prompt with mode detection.
    Switches between extraction and explanation modes based on query type.
    """
    context = "\n\n".join(retrieved_chunks)
    
    # Check if this is a policy extraction query
    if any(term in query.lower() for term in ['what are covered', 'policy', 'jlmt', 'objectives', 'scope', 'stipend']):
        prompt = f"""Extract and reproduce the policy information verbatim from the context below.
Preserve section numbering, headings, and bullet points exactly as written.
Do not add information that is not explicitly present in the context.
If the context doesn't contain specific policy details, say "The context doesn't contain the specific policy information requested."

Context:
{context}

Question: {query}

Answer:"""
    else:
        prompt = f"""You are a helpful Jindal Power assistant. Answer questions based only on the provided context.

Context:
{context}

Question: {query}

Provide a clear, helpful answer using only the information above. If the context doesn't contain the answer, say "I don't have enough information to answer this question."

Answer:"""
    
    return prompt


def build_context_prompt(session_id: str, current_query: str, retrieved_chunks: List[str]) -> str:
    """
    Build prompt with conversation context (legacy function for compatibility).
    """
    context = "\n\n".join(retrieved_chunks)
    
    prompt = f"""You are a helpful Jindal Power assistant. Answer the current question based on the provided document context and conversation history.

Document Context:
{document_context}

Current Question: {current_query}

Provide a clear, helpful answer using the information above. If the context doesn't contain the answer, say "I don't have enough information to answer this question."

Answer:"""
    
    return prompt

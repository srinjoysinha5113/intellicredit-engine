"""
Chat API endpoint.
"""

import asyncio
import json
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.schemas import ChatRequest, ChatResponse
from sessions.memory import get_or_create_session, add_message_to_session, sessions
from retrieval.retriever import retrieve_relevant_chunks
from rag.prompts import build_rag_prompt
from config import LLM_MODEL, LLM_OPTIONS, MAX_CONCURRENT_LLM_CALLS, DEFAULT_RETRIEVAL_K, CHUNK_MIN_WORDS, MAX_MESSAGE_LENGTH
import ollama

router = APIRouter()

# Semaphore to limit concurrent LLM calls
llm_semaphore = asyncio.Semaphore(MAX_CONCURRENT_LLM_CALLS)

# Global variables (will be set during startup)
vector_store = None
chunks_db = None


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main RAG chat endpoint with session context.
    """
    global vector_store, chunks_db

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    if len(request.message) > MAX_MESSAGE_LENGTH:
        raise HTTPException(status_code=400, detail=f"Message too long (max {MAX_MESSAGE_LENGTH} characters)")

    # Get or create session
    session_id = get_or_create_session(request.session_id)
    
    # Add user message to session
    add_message_to_session(session_id, "user", request.message)

    # Check if this is a follow-up message (has conversation history)
    session = sessions.get(session_id, {})
    conversation_history = session.get("messages", [])
    
    # For follow-up messages or document queries, always use RAG

    if vector_store is None or not chunks_db:
        raise HTTPException(status_code=503, detail="Vector store not initialized. No documents loaded?")

    # Retrieve relevant chunks for specific queries
    retrieved_chunks = retrieve_relevant_chunks(request.message, vector_store, chunks_db, k=DEFAULT_RETRIEVAL_K)

    if not retrieved_chunks:
        error_msg = "I don't have specific information about that in the Jindal Power documents. Could you try rephrasing your question or ask about policies, procedures, or company guidelines?"
        add_message_to_session(session_id, "bot", error_msg)
        return ChatResponse(
            answer=error_msg,
            source_chunks=[],
            session_id=session_id
        )

    # Build RAG prompt
    prompt = build_rag_prompt(request.message, retrieved_chunks)

    # Call Ollama with semaphore for concurrency control
    async with llm_semaphore:
        try:
            response = await asyncio.to_thread(
                ollama.chat,
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                options=LLM_OPTIONS
            )

            answer = response["message"]["content"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    # Add bot response to session
    add_message_to_session(session_id, "bot", answer)

    return ChatResponse(
        answer=answer,
        source_chunks=retrieved_chunks[:2],  # Return top 2 chunks
        session_id=session_id
    )


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming RAG chat endpoint with real-time token delivery.
    """
    global vector_store, chunks_db

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    if len(request.message) > MAX_MESSAGE_LENGTH:
        raise HTTPException(status_code=400, detail=f"Message too long (max {MAX_MESSAGE_LENGTH} characters)")

    # Get or create session
    session_id = get_or_create_session(request.session_id)
    
    # Add user message to session
    add_message_to_session(session_id, "user", request.message)

    if vector_store is None or not chunks_db:
        raise HTTPException(status_code=503, detail="Vector store not initialized. No documents loaded?")

    # Retrieve relevant chunks
    retrieved_chunks = retrieve_relevant_chunks(request.message, vector_store, chunks_db, k=DEFAULT_RETRIEVAL_K)

    async def generate_response():
        try:
            if not retrieved_chunks:
                error_msg = "I don't have specific information about that in the Jindal Power documents. Could you try rephrasing your question or ask about policies, procedures, or company guidelines?"
                yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"
                add_message_to_session(session_id, "bot", error_msg)
                return

            # Build RAG prompt
            prompt = build_rag_prompt(request.message, retrieved_chunks)
            
            # Send start signal
            yield f"data: {json.dumps({'type': 'start', 'session_id': session_id})}\n\n"
            
            full_response = ""
            
            # Stream LLM response
            async with llm_semaphore:
                response_stream = await asyncio.to_thread(
                    ollama.chat,
                    model=LLM_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    options=LLM_OPTIONS,
                    stream=True
                )
                
                for chunk in response_stream:
                    if 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        full_response += content
                        
                        # Send chunk to frontend
                        yield f"data: {json.dumps({'type': 'chunk', 'content': content})}\n\n"
                        
                        # Small delay for better streaming effect
                        await asyncio.sleep(0.01)
            
            # Send completion signal with sources
            yield f"data: {json.dumps({'type': 'end', 'content': full_response, 'sources': retrieved_chunks[:2]})}\n\n"
            
            # Add full response to session
            add_message_to_session(session_id, "bot", full_response)
            
        except Exception as e:
            error_msg = f"Streaming error: {str(e)}"
            yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"

    return StreamingResponse(
        generate_response(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )

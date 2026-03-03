"""
Session memory management.
"""

import asyncio
from typing import Dict, List, Optional
from uuid import uuid4


# In-memory session store (can be replaced with Redis later)
sessions: Dict[str, Dict] = {}


def get_or_create_session(session_id: Optional[str]) -> str:
    """Get existing session or create new one. Returns session_id."""
    if session_id and session_id in sessions:
        return session_id
    
    # Create new session
    new_session_id = str(uuid4())
    sessions[new_session_id] = {
        "messages": [],
        "created_at": asyncio.get_event_loop().time()
    }
    return new_session_id


def add_message_to_session(session_id: str, role: str, content: str):
    """Add message to session and maintain window of last 10 messages."""
    if session_id not in sessions:
        return
    
    sessions[session_id]["messages"].append({
        "role": role,
        "content": content
    })
    
    # Keep only last 10 messages
    if len(sessions[session_id]["messages"]) > 10:
        sessions[session_id]["messages"] = sessions[session_id]["messages"][-10:]


def get_conversation_history_for_llm(session_id: str) -> str:
    """Format conversation history for LLM context."""
    if session_id not in sessions:
        return ""
    
    messages = sessions[session_id]["messages"]
    if not messages:
        return ""
    
    # Exclude the last message (current user query) and format history
    history_messages = messages[:-1] if len(messages) > 1 else []
    
    if not history_messages:
        return ""
    
    history_lines = []
    for msg in history_messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_lines.append(f"{role}: {msg['content']}")
    
    return "\n".join(history_lines)

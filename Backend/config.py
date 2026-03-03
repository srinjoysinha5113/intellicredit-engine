"""
Configuration settings and constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Data and index paths
DATA_DIR = os.getenv("DATA_DIR", "./data")
INDEX_DIR = os.getenv("INDEX_DIR", "./faiss_index")
EMBEDDINGS_FILE = os.path.join(INDEX_DIR, os.getenv("EMBEDDINGS_FILE", "embeddings.pkl"))
CHUNKS_FILE = os.path.join(INDEX_DIR, os.getenv("CHUNKS_FILE", "chunks.pkl"))

# Model settings
EMBED_MODEL = os.getenv("EMBED_MODEL", "mxbai-embed-large")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:1b")

# LLM options
LLM_OPTIONS = {
    "temperature": float(os.getenv("LLM_TEMPERATURE", "0.3")),
    "top_p": float(os.getenv("LLM_TOP_P", "0.9")),
    "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "300"))
}

# OCR settings
TESSERACT_PATH = os.getenv("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
POPPLER_PATH = os.getenv("POPPLER_PATH", r"C:\Program Files\poppler-25.12.0\Library\bin")

# API Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "1000"))
MAX_CONCURRENT_LLM_CALLS = int(os.getenv("MAX_CONCURRENT_LLM_CALLS", "3"))

# Retrieval Configuration
DEFAULT_RETRIEVAL_K = int(os.getenv("DEFAULT_RETRIEVAL_K", "8"))
CHUNK_MIN_WORDS = int(os.getenv("CHUNK_MIN_WORDS", "10"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "300"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

# Response templates
RESPONSES = {
    "greeting": "Hello! I'm here to help you with Jindal Power policies and procedures. What would you like to know today?",
    "bot_identity": "I'm the Jindal Power Assistant, an AI chatbot trained to help employees with company policies, procedures, and information.",
    "bot_capabilities": "I can help you with information about Jindal Power policies, leave procedures, travel expenses, HR guidelines, and other company-related questions.",
    "help_request": "I'm here to help! You can ask me about Jindal Power policies, leave procedures, travel expenses, or any other company-related questions.",
    "command_reset": "Starting a new conversation. How can I assist you today?",
    "command_stop": "Okay, I'll stop. Is there anything else I can help with?",
    "politeness": "You're welcome! I'm here to help.",
    "acknowledgement": "Understood.",
    "confirmation_yes": "Great!",
    "confirmation_no": "Okay, let me know if you change your mind.",
    "exit_conversation": "Goodbye! Have a great day."
}

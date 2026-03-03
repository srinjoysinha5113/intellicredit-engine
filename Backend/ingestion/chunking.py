"""
Text chunking strategies for different document types.
"""

import re
from typing import List


def split_text_into_chunks(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    """
    Simple recursive text splitter.
    """
    chunks = []
    words = text.split()

    i = 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    
    return chunks


def split_text_by_sections(text: str) -> List[str]:
    """
    Split text by section headers (e.g., "1.0", "2.0", etc.).
    Useful for policy documents with numbered sections.
    """
    sections = []
    # Split on numbered section headers
    section_pattern = r'(\d+\.\d+\s+.+?)(?=\d+\.\d+\s+|\Z)'
    matches = re.findall(section_pattern, text, re.DOTALL)
    
    if matches:
        sections = [match.strip() for match in matches if match.strip()]
    
    # Fallback to regular chunking if no sections found
    if not sections:
        sections = split_text_into_chunks(text, chunk_size=400, overlap=75)
    
    return sections

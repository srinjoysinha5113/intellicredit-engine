"""
CSV file ingestion.
Handles various encodings and formats.
"""

import csv
from typing import List, Optional

from config import CHUNK_SIZE, CHUNK_OVERLAP
from ingestion.chunking import split_text_into_chunks
from models.schemas import KnowledgeChunk


def process_csv_file(file_path: str, file: str, relative_path: str, category: str, subcategory: str) -> List[KnowledgeChunk]:
    """Extract text from CSV files and create KnowledgeChunk objects."""
    chunks = []
    
    def _read_csv(encoding: str) -> Optional[List[List[str]]]:
        try:
            with open(file_path, mode="r", encoding=encoding, newline="") as f:
                reader = csv.reader(f)
                return [[str(cell).strip() for cell in row if str(cell).strip()] for row in reader]
        except Exception:
            return None

    rows = _read_csv("utf-8")
    if rows is None:
        rows = _read_csv("utf-8-sig")
    if rows is None:
        rows = _read_csv("cp1252")
    
    if not rows:
        print(f"No data extracted from CSV: {file}")
        return chunks
    
    # Convert rows to text lines
    text_lines = []
    for row in rows:
        if row:  # Skip empty rows
            line = " | ".join(row)  # Join columns with separator
            text_lines.append(line)
    
    if text_lines:
        full_text = f"CSV File: {file}\n" + "\n".join(text_lines)
        csv_chunks = split_text_into_chunks(full_text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
        
        for chunk in csv_chunks:
            knowledge_chunk = KnowledgeChunk(
                content=chunk,
                source_type="csv",
                source_name=file,
                source_path=relative_path,
                metadata={"category": category, "subcategory": subcategory},
                structure={"format": "csv"}
            )
            chunks.append(knowledge_chunk)
    
    return chunks

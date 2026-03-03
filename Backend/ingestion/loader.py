"""
Document loader and orchestrator.
Handles directory traversal and coordinates different file type processors.
"""

import os
from typing import List

from ingestion.pdf import process_pdf_file
from ingestion.excel import process_excel_file
from ingestion.csv import process_csv_file
from ingestion.pptx import process_pptx_file
from models.schemas import KnowledgeChunk


def ingest_documents(data_dir: str) -> List[KnowledgeChunk]:
    """
    Load all documents (PDFs, Excel, PowerPoint, CSV) from data/ folder recursively.
    Extract text and create KnowledgeChunk objects.
    Returns a list of KnowledgeChunk without performing embeddings or FAISS indexing.
    """
    all_chunks = []

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created {data_dir} folder. Please add your documents here.")

    # Recursive traversal using os.walk
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.lower().endswith((".pdf", ".xlsx", ".xls", ".csv", ".pptx")):
                file_path = os.path.join(root, file)
                # Compute relative path from DATA_DIR
                relative_path = os.path.relpath(file_path, data_dir)
                # Extract category and subcategory from relative path
                path_parts = relative_path.split(os.sep)
                if len(path_parts) >= 2:
                    category = path_parts[0]
                    subcategory = path_parts[1] if len(path_parts) > 2 else None
                else:
                    # Flat file in root
                    category = "General"
                    subcategory = None

                # Process based on file type
                if file.lower().endswith(".pdf"):
                    print(f"Processing PDF: {file_path}")
                    chunks = process_pdf_file(file_path, file, relative_path, category, subcategory)
                elif file.lower().endswith((".xlsx", ".xls")):
                    print(f"Processing Excel: {file_path}")
                    chunks = process_excel_file(file_path, file, relative_path, category, subcategory)
                elif file.lower().endswith(".csv"):
                    print(f"Processing CSV: {file_path}")
                    chunks = process_csv_file(file_path, file, relative_path, category, subcategory)
                elif file.lower().endswith(".pptx"):
                    print(f"Processing PowerPoint: {file_path}")
                    chunks = process_pptx_file(file_path, file, relative_path, category, subcategory)
                else:
                    continue
                all_chunks.extend(chunks)
    return all_chunks

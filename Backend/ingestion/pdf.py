"""
PDF ingestion with OCR support.
Handles native text extraction and OCR fallback for scanned PDFs.
"""

import os
import re
from typing import List, Tuple, Optional
import PyPDF2
import pytesseract
from PIL import Image
import pdf2image
import numpy as np
from config import TESSERACT_PATH, POPPLER_PATH, CHUNK_SIZE, CHUNK_OVERLAP

from ingestion.chunking import split_text_into_chunks
from models.schemas import KnowledgeChunk


def extract_text_with_ocr(pdf_path: str, page_num: int = 0) -> str:
    """
    Extract text from a specific PDF page using OCR.
    Converts only the specified page to image for OCR processing.
    """
    try:
        # Set Tesseract path from config
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        
        # Set Poppler path from config
        poppler_path = POPPLER_PATH
        
        # Convert only the specific page to image
        images = pdf2image.convert_from_path(
            pdf_path, 
            first_page=page_num + 1, 
            last_page=page_num + 1,
            poppler_path=poppler_path
        )
        
        if not images:
            print(f"No image generated for page {page_num + 1}")
            return ""
        
        # Extract text from the page image
        image = images[0]
        text = pytesseract.image_to_string(image, config='--psm 6')
        
        print(f"OCR processed page {page_num + 1}, extracted {len(text)} characters")
        return text.strip()
        
    except Exception as e:
        print(f"Error processing page {page_num + 1} with OCR: {e}")
        return ""


def extract_text_unified(pdf_path: str, page, page_num: int) -> Tuple[str, bool]:
    """
    Extract text from PDF page with OCR fallback.
    Returns (text, used_ocr_flag)
    """
    # Try native text extraction first
    try:
        native_text = page.extract_text()
        if native_text and len(native_text.strip()) > 100:
            return native_text.strip(), False
    except Exception as e:
        print(f"Native text extraction failed for page {page_num + 1}: {e}")
    
    # Fallback to OCR if native text is insufficient
    print(f"Starting OCR processing for {pdf_path} (page {page_num + 1})")
    ocr_text = extract_text_with_ocr(pdf_path, page_num)
    
    if ocr_text and len(ocr_text.strip()) > 50:
        return ocr_text, True
    
    return "", False


def assess_text_usability(text: str, used_ocr: bool) -> str:
    """
    Assess if extracted text is sufficient for answering questions.
    Returns 'answerable' or 'reference_only'.
    """
    if not text or len(text.strip()) < 50:
        return "reference_only"
    
    length = len(text)
    sentences = re.split(r'[.!?]+', text)
    sentence_count = sum(1 for s in sentences if s.strip())

    if used_ocr:
        # Stricter for OCR: longer text and more sentences
        if length > 200 and sentence_count > 5:
            return "answerable"
        else:
            return "reference_only"
    else:
        # For native text
        if length > 100 and sentence_count > 3:
            return "answerable"
        else:
            return "reference_only"


def process_pdf_file(file_path: str, file: str, relative_path: str, category: str, subcategory: str) -> List[KnowledgeChunk]:
    """Process PDF file and create KnowledgeChunk objects."""
    chunks = []
    
    try:
        reader = PyPDF2.PdfReader(file_path)
        for page_num, page in enumerate(reader.pages):
            text, used_ocr = extract_text_unified(file_path, page, page_num)
            if text.strip():
                capability = assess_text_usability(text, used_ocr)
                # Split page into chunks
                page_chunks = split_text_into_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
                for chunk in page_chunks:
                    knowledge_chunk = KnowledgeChunk(
                        content=chunk,
                        source_type="pdf",
                        source_name=file,
                        source_path=relative_path,
                        metadata={"category": category, "subcategory": subcategory, "capability": capability, "ocr_used": used_ocr},
                        structure={"page": page_num + 1}
                    )
                    chunks.append(knowledge_chunk)
        
    except Exception as e:
        print(f"Error processing PDF file {file}: {str(e)}")
    
    return chunks

"""
Parsing Module - Converts PDF files to plain text.

Uses PyMuPDF (fitz) for reliable text extraction from PDF resumes.

Functions:
    - extract_text_from_pdf(): Read text from a PDF file path
    - extract_text_from_bytes(): Read text from raw PDF bytes
"""

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text content from a PDF file.

    Args:
        pdf_path: Path to the PDF file on disk

    Returns:
        Extracted text as a single string (pages joined)
    """
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"[ERROR] Error reading PDF '{pdf_path}': {e}")
        return ""
    return text.strip()


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF given as raw bytes (useful for uploads).

    Args:
        pdf_bytes: Raw bytes of the PDF file

    Returns:
        Extracted text as a single string
    """
    text = ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"[ERROR] Error reading PDF bytes: {e}")
        return ""
    return text.strip()

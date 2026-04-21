"""
Ingestion Module - Handles file upload and storage.

Functions:
    - save_resume(): Save uploaded PDF to temp directory
    - get_all_resumes(): List all uploaded resume paths
    - cleanup_temp(): Delete all temporary files
"""

import os
import shutil
from pathlib import Path


# ─── Directory Paths ───────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / "temp_resumes"
OUTPUT_DIR = BASE_DIR / "outputs"


def ensure_directories():
    """Create necessary directories if they don't exist."""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_resume(file_bytes: bytes, filename: str) -> str:
    """
    Save an uploaded resume PDF to the temp_resumes/ directory.

    Args:
        file_bytes: Raw bytes of the PDF file
        filename: Original filename of the PDF

    Returns:
        Full path to the saved file as a string
    """
    ensure_directories()
    filepath = TEMP_DIR / filename
    with open(filepath, "wb") as f:
        f.write(file_bytes)
    return str(filepath)


def get_all_resumes() -> list:
    """
    Get paths of all PDF files in the temp_resumes/ directory.

    Returns:
        List of file path strings
    """
    ensure_directories()
    return [str(f) for f in TEMP_DIR.glob("*.pdf")]


def cleanup_temp():
    """Delete all files in temp_resumes/ directory."""
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    print("[DONE] Temporary files cleaned up.")

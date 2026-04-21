"""
Embeddings Module - Converts text to numerical vectors.

Uses sentence-transformers (all-MiniLM-L6-v2) to generate semantic embeddings.
The model maps text to a 384-dimensional dense vector space.

Functions:
    - get_model(): Load and cache the transformer model (singleton)
    - generate_embedding(): Convert a single text to a vector
    - generate_embeddings_batch(): Convert multiple texts to vectors
"""

import numpy as np
from sentence_transformers import SentenceTransformer


# ─── Singleton Model Instance ──────────────────────────────────
_model = None


def get_model() -> SentenceTransformer:
    """
    Load and cache the sentence transformer model.
    Downloads the model on first run (~80MB).

    Returns:
        SentenceTransformer model instance
    """
    global _model
    if _model is None:
        print("[LOADING] Loading embedding model (all-MiniLM-L6-v2)...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("[DONE] Model loaded successfully.")
    return _model


def generate_embedding(text: str) -> np.ndarray:
    """
    Convert a single text string to a numerical vector.

    Args:
        text: Input text (resume or job description)

    Returns:
        Numpy array of shape (384,) — the embedding vector
    """
    model = get_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return np.array(embedding, dtype=np.float32)


def generate_embeddings_batch(texts: list) -> np.ndarray:
    """
    Convert multiple texts to embeddings in a single batch (faster).

    Args:
        texts: List of text strings

    Returns:
        Numpy array of shape (n, 384)
    """
    model = get_model()
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    return np.array(embeddings, dtype=np.float32)

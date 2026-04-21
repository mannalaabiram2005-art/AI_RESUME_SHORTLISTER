"""
Matching Module - Compares resume embeddings with job description.

Uses FAISS (Facebook AI Similarity Search) for efficient vector comparison.
Since embeddings are L2-normalized, Inner Product = Cosine Similarity.

Functions:
    - compute_cosine_similarity(): Compare two vectors directly
    - build_faiss_index(): Build a searchable index from resume embeddings
    - search_similar(): Find top-K similar resumes to a query
    - match_resumes_to_job(): Get similarity scores for all resumes vs JD
"""

import numpy as np
import faiss


def compute_cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.

    Args:
        vec_a: First vector (e.g., resume embedding)
        vec_b: Second vector (e.g., JD embedding)

    Returns:
        Similarity score between 0.0 and 1.0
    """
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))


def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    """
    Build a FAISS index from resume embeddings.
    Uses Inner Product (IP) — equivalent to cosine similarity
    for L2-normalized vectors.

    Args:
        embeddings: Numpy array of shape (num_resumes, embedding_dim)

    Returns:
        FAISS index ready for searching
    """
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index


def search_similar(index: faiss.IndexFlatIP, query_embedding: np.ndarray, top_k: int = 10):
    """
    Search the FAISS index for most similar resumes to the JD.

    Args:
        index: FAISS index built from resume embeddings
        query_embedding: Job description embedding, shape (dim,)
        top_k: Number of top results to return

    Returns:
        Tuple of (scores_array, indices_array)
    """
    query = query_embedding.reshape(1, -1)
    k = min(top_k, index.ntotal)
    scores, indices = index.search(query, k)
    return scores[0], indices[0]


def match_resumes_to_job(resume_embeddings: np.ndarray, job_embedding: np.ndarray) -> list:
    """
    Match all resumes against a job description using FAISS.

    Args:
        resume_embeddings: Array of shape (num_resumes, dim)
        job_embedding: Array of shape (dim,)

    Returns:
        List of similarity scores (one per resume, in original order)
    """
    n = len(resume_embeddings)
    index = build_faiss_index(resume_embeddings)
    scores, indices = search_similar(index, job_embedding, top_k=n)

    # Map scores back to original resume order
    result = [0.0] * n
    for score, idx in zip(scores, indices):
        if 0 <= idx < n:
            result[int(idx)] = round(float(score), 4)

    return result

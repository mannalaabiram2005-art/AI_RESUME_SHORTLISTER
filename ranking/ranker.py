"""
Ranking Module - Sorts candidates by their final scores.

Functions:
    - rank_candidates(): Sort all candidates, assign rank numbers
    - get_top_candidates(): Get the top N candidates
    - get_shortlisted(): Get candidates above a score threshold
"""


def rank_candidates(candidates: list) -> list:
    """
    Sort candidates by final_score (highest first) and assign rank numbers.

    Args:
        candidates: List of dicts, each must have a 'final_score' key

    Returns:
        New sorted list with 'rank' field added to each candidate
    """
    sorted_candidates = sorted(
        candidates,
        key=lambda x: x.get("final_score", 0),
        reverse=True,
    )
    for i, candidate in enumerate(sorted_candidates, start=1):
        candidate["rank"] = i
    return sorted_candidates


def get_top_candidates(candidates: list, top_n: int = 5) -> list:
    """
    Get the top N candidates by score.

    Args:
        candidates: List of candidate dicts
        top_n: How many to return (default 5)

    Returns:
        List of top N ranked candidates
    """
    ranked = rank_candidates(candidates)
    return ranked[:top_n]


def get_shortlisted(candidates: list, threshold: float = 60.0) -> list:
    """
    Get candidates whose final_score is at or above the threshold.

    Args:
        candidates: List of candidate dicts
        threshold: Minimum score to be shortlisted (default 60.0)

    Returns:
        List of shortlisted candidates (ranked)
    """
    ranked = rank_candidates(candidates)
    return [c for c in ranked if c.get("final_score", 0) >= threshold]

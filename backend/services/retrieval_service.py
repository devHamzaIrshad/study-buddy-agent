from typing import List, Tuple
from backend.storage.in_memory_store import DocChunk

def score_chunk_optimized(query_tokens: List[str], text_lower: str) -> float:
    """Optimized keyword overlap scoring."""
    score = 0.0
    for w in query_tokens:
        if w in text_lower:
            score += 1.0
    return score

def retrieve_top_k(query: str, chunks: List[DocChunk], top_k: int) -> List[Tuple[DocChunk, float]]:
    # Pre-process query once
    query_tokens = [w for w in query.lower().split() if len(w) > 2]
    if not query_tokens:
        return []

    scored = []
    for ch in chunks:
        # Pre-process chunk text if not already lowercased (or assume it's small enough)
        s = score_chunk_optimized(query_tokens, ch.text.lower())
        if s > 0:
            scored.append((ch, s))
            
    # Sort and return
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
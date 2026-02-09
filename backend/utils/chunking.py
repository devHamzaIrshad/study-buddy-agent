"""
Enhanced text chunking with sentence-aware splitting and validation.
"""
from typing import Generator, List
import re


def split_into_sentences(text: str) -> List[str]:
    """
    Splits text into sentences using basic punctuation rules.
    
    Args:
        text: Text to split
        
    Returns:
        List of sentences
    """
    # Simple sentence splitting on common punctuation
    # This handles most cases without needing heavy NLP libraries
    sentence_endings = re.compile(r'([.!?]+[\s\n]+)')
    sentences = sentence_endings.split(text)
    
    # Recombine sentences with their punctuation
    result = []
    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else '')
        if sentence.strip():
            result.append(sentence.strip())
    
    # Add last sentence if it doesn't end with punctuation
    if sentences and not sentence_endings.search(sentences[-1]):
        if sentences[-1].strip():
            result.append(sentences[-1].strip())
    
    return result if result else [text]


def chunk_text(
    text: str,
    chunk_size: int,
    overlap: int,
    sentence_aware: bool = True
) -> Generator[str, None, None]:
    """
    Yields text chunks with optional sentence-aware splitting.
    More memory-efficient than building a full list.
    
    Args:
        text: Text to chunk
        chunk_size: Target size for each chunk (in characters)
        overlap: Number of characters to overlap between chunks
        sentence_aware: If True, tries to break at sentence boundaries
        
    Yields:
        Text chunks
    """
    if chunk_size <= 0:
        yield text
        return
        
    if overlap >= chunk_size:
        overlap = max(0, chunk_size // 3)
    
    # If sentence-aware chunking is enabled and text is not too large
    if sentence_aware and len(text) < chunk_size * 100:
        sentences = split_into_sentences(text)
        
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_len = len(sentence)
            
            # If adding this sentence would exceed chunk size
            if current_size + sentence_len > chunk_size and current_chunk:
                # Yield current chunk
                chunk_text = ' '.join(current_chunk)
                if chunk_text.strip():
                    yield chunk_text.strip()
                
                # Start new chunk with overlap
                # Keep last few sentences for context
                overlap_text = ' '.join(current_chunk)
                if len(overlap_text) > overlap:
                    # Find sentences that fit in overlap
                    overlap_sentences = []
                    overlap_size = 0
                    for s in reversed(current_chunk):
                        if overlap_size + len(s) <= overlap:
                            overlap_sentences.insert(0, s)
                            overlap_size += len(s)
                        else:
                            break
                    current_chunk = overlap_sentences
                    current_size = overlap_size
                else:
                    current_chunk = []
                    current_size = 0
            
            # Add sentence to current chunk
            current_chunk.append(sentence)
            current_size += sentence_len
        
        # Yield final chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            if chunk_text.strip():
                yield chunk_text.strip()
    
    else:
        # Fall back to character-based chunking for very large texts
        start = 0
        n = len(text)
        
        while start < n:
            end = min(n, start + chunk_size)
            chunk = text[start:end].strip()
            if chunk:
                yield chunk
            start = end - overlap
            if start < 0:
                start = 0
            if start >= n:
                break


def validate_chunk(chunk: str, min_length: int = 10) -> bool:
    """
    Validates that a chunk meets minimum quality standards.
    
    Args:
        chunk: Text chunk to validate
        min_length: Minimum acceptable length
        
    Returns:
        True if chunk is valid
    """
    if not chunk or not chunk.strip():
        return False
    
    if len(chunk.strip()) < min_length:
        return False
    
    # Check if chunk has some meaningful content (not just whitespace/special chars)
    alphanumeric_count = sum(c.isalnum() for c in chunk)
    if alphanumeric_count < min_length // 2:
        return False
    
    return True

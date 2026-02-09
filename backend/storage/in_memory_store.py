from dataclasses import dataclass
from typing import Dict, List, Optional
import sys


@dataclass
class DocChunk:
    doc_id: str
    doc_name: str
    chunk_id: int
    text: str


class InMemoryStore:
    """
    Stores documents and chunks in memory (per Streamlit session).
    Enhanced with memory tracking and statistics.
    """
    def __init__(self) -> None:
        self.docs: Dict[str, str] = {}          # doc_id -> doc_name
        self.chunks: Dict[str, List[DocChunk]] = {}  # doc_id -> list of chunks

    def upsert_doc(self, doc_id: str, doc_name: str, chunks: List[DocChunk]) -> None:
        """Add or update a document with its chunks."""
        self.docs[doc_id] = doc_name
        self.chunks[doc_id] = chunks

    def list_docs(self) -> List[tuple]:
        """List all documents as (doc_id, doc_name) tuples."""
        return [(doc_id, name) for doc_id, name in self.docs.items()]

    def get_chunks(self, doc_id: str) -> List[DocChunk]:
        """Get all chunks for a specific document."""
        return self.chunks.get(doc_id, [])

    def remove_doc(self, doc_id: str) -> None:
        """Remove a document and its chunks."""
        self.docs.pop(doc_id, None)
        self.chunks.pop(doc_id, None)
    
    def get_total_chunks(self) -> int:
        """Get total number of chunks across all documents."""
        return sum(len(chunks) for chunks in self.chunks.values())
    
    def get_memory_usage_mb(self) -> float:
        """
        Estimate memory usage of stored documents in MB.
        This is an approximation based on text size.
        """
        total_bytes = 0
        for chunks in self.chunks.values():
            for chunk in chunks:
                # Estimate size of chunk text
                total_bytes += sys.getsizeof(chunk.text)
        return total_bytes / (1024 * 1024)
    
    def get_statistics(self) -> Dict:
        """Get storage statistics."""
        return {
            "total_docs": len(self.docs),
            "total_chunks": self.get_total_chunks(),
            "memory_mb": round(self.get_memory_usage_mb(), 2),
            "docs": [
                {
                    "doc_id": doc_id,
                    "doc_name": self.docs[doc_id],
                    "num_chunks": len(self.chunks.get(doc_id, []))
                }
                for doc_id in self.docs.keys()
            ]
        }

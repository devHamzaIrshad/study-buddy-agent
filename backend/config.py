import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    groq_api_key: str = os.environ.get("GROQ_API_KEY", "")
    groq_model: str = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

    max_context_chars: int = int(os.environ.get("MAX_CONTEXT_CHARS", "14000"))
    chunk_size: int = int(os.environ.get("CHUNK_SIZE", "1200"))
    chunk_overlap: int = int(os.environ.get("CHUNK_OVERLAP", "200"))
    top_k: int = int(os.environ.get("TOP_K", "5"))
    
    # File upload limits for memory management
    max_file_size_mb: float = float(os.environ.get("MAX_FILE_SIZE_MB", "50"))
    max_pdf_pages: int = int(os.environ.get("MAX_PDF_PAGES", "500"))
    
    # PDF processing configuration
    pdf_batch_size: int = int(os.environ.get("PDF_BATCH_SIZE", "10"))  # Pages per batch for GC

settings = Settings()
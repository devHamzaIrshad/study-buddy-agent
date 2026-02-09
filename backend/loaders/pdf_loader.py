"""
Memory-efficient PDF loader with streaming processing and robust error handling.
"""
from typing import Union, Optional, Callable, List
import io
import gc
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from backend.utils.text_clean import clean_text
from backend.utils.file_validator import validate_file_size, FileValidationError
from backend.utils.error_handler import PDFProcessingError, log_error


def validate_pdf_integrity(file_obj: io.BytesIO, filename: str = "PDF") -> None:
    """
    Validates PDF file integrity before processing.
    
    Args:
        file_obj: BytesIO object containing PDF data
        filename: Name of the file for error messages
        
    Raises:
        PDFProcessingError: If PDF is corrupted or invalid
    """
    try:
        # Try to create a reader to check if PDF is valid
        current_pos = file_obj.tell()
        reader = PdfReader(file_obj)
        
        # Check if PDF has pages
        if len(reader.pages) == 0:
            raise PDFProcessingError("PDF file is empty (no pages found)", filename)
        
        # Reset position
        file_obj.seek(current_pos)
        
    except PdfReadError as e:
        raise PDFProcessingError(f"Corrupted or invalid PDF file: {str(e)}", filename)
    except Exception as e:
        raise PDFProcessingError(f"Unable to read PDF: {str(e)}", filename)


def extract_text_from_page(page, page_num: int, filename: str) -> str:
    """
    Safely extracts text from a single PDF page with error handling.
    
    Args:
        page: PDF page object
        page_num: Page number (0-indexed)
        filename: Filename for error messages
        
    Returns:
        Extracted text or empty string if extraction fails
    """
    try:
        text = page.extract_text()
        return text if text else ""
    except Exception as e:
        log_error(e, f"Page {page_num + 1} of {filename}")
        # Return empty string instead of failing completely
        return ""


def read_pdf_bytes(
    file_obj: Union[bytes, io.BytesIO],
    max_size_mb: float = 50.0,
    max_pages: Optional[int] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    batch_size: int = 10
) -> str:
    """
    Reads PDF from bytes with memory-efficient streaming and robust error handling.
    
    Args:
        file_obj: PDF file as bytes or BytesIO object
        max_size_mb: Maximum allowed file size in MB (default: 50MB)
        max_pages: Maximum number of pages to process (None = all pages)
        progress_callback: Optional callback function(current_page, total_pages)
        batch_size: Number of pages to process before garbage collection
        
    Returns:
        Cleaned text extracted from the PDF
        
    Raises:
        FileValidationError: If file exceeds size limit
        PDFProcessingError: If PDF processing fails
        
    Memory Optimization:
        - Processes pages in batches with explicit garbage collection
        - Validates file before processing to prevent memory issues
        - Uses streaming text accumulation
        - Cleans up page objects immediately after use
    """
    filename = "PDF"
    
    try:
        # Validate file size first to prevent memory issues
        validate_file_size(file_obj, max_size_mb=max_size_mb, filename=filename)
        
        # Convert bytes to BytesIO if needed
        if isinstance(file_obj, bytes):
            file_obj = io.BytesIO(file_obj)
        
        # Validate PDF integrity
        validate_pdf_integrity(file_obj, filename)
        
        # Create reader
        reader = PdfReader(file_obj)
        total_pages = len(reader.pages)
        
        # Limit pages if specified
        pages_to_process = min(total_pages, max_pages) if max_pages else total_pages
        
        if pages_to_process == 0:
            raise PDFProcessingError("No pages to process", filename)
        
        # Process pages with streaming and batch garbage collection
        text_parts: List[str] = []
        failed_pages: List[int] = []
        
        for page_num in range(pages_to_process):
            try:
                # Extract text from single page
                page = reader.pages[page_num]
                page_text = extract_text_from_page(page, page_num, filename)
                
                if page_text and page_text.strip():
                    text_parts.append(page_text)
                else:
                    # Track pages with no text
                    failed_pages.append(page_num + 1)
                
                # Call progress callback if provided
                if progress_callback:
                    try:
                        progress_callback(page_num + 1, pages_to_process)
                    except Exception as e:
                        log_error(e, "Progress callback")
                
                # Clean up page object to free memory
                del page
                
                # Batch garbage collection for memory efficiency
                if (page_num + 1) % batch_size == 0:
                    gc.collect()
                    
            except Exception as e:
                # Log error but continue processing other pages
                log_error(e, f"Page {page_num + 1} of {filename}")
                failed_pages.append(page_num + 1)
                continue
        
        # Check if we extracted any text
        if not text_parts:
            raise PDFProcessingError(
                "No text could be extracted from PDF. It might be image-based or corrupted.",
                filename
            )
        
        # Join all text parts
        full_text = "\n\n".join(text_parts)
        
        # Log warning if some pages failed
        if failed_pages and len(failed_pages) < pages_to_process:
            print(f"⚠️ Warning: {len(failed_pages)} page(s) could not be processed: {failed_pages[:10]}")
        
        # Clean up
        del text_parts
        del reader
        gc.collect()
        
        # Clean and return text
        cleaned_text = clean_text(full_text)
        
        if not cleaned_text or len(cleaned_text.strip()) < 10:
            raise PDFProcessingError(
                "PDF processed but no meaningful text found",
                filename
            )
        
        return cleaned_text
        
    except (FileValidationError, PDFProcessingError):
        # Re-raise our custom errors
        raise
    except Exception as e:
        # Wrap unexpected errors
        log_error(e, "PDF processing")
        raise PDFProcessingError(f"Unexpected error: {str(e)}", filename)


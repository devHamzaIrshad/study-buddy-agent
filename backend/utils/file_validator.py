"""
File validation utilities for upload safety and memory management.
"""
from typing import Optional, Union
import io


class FileValidationError(Exception):
    """Raised when file validation fails."""
    pass


def get_file_size_mb(file_obj: Union[bytes, io.BytesIO]) -> float:
    """
    Gets file size in megabytes.
    
    Args:
        file_obj: File bytes or BytesIO object
        
    Returns:
        File size in MB
    """
    if isinstance(file_obj, bytes):
        size_bytes = len(file_obj)
    elif isinstance(file_obj, io.BytesIO):
        current_pos = file_obj.tell()
        file_obj.seek(0, 2)  # Seek to end
        size_bytes = file_obj.tell()
        file_obj.seek(current_pos)  # Restore position
    else:
        # For uploaded file objects with size attribute
        size_bytes = getattr(file_obj, 'size', 0)
    
    return size_bytes / (1024 * 1024)


def validate_file_size(
    file_obj: Union[bytes, io.BytesIO],
    max_size_mb: float = 50.0,
    filename: str = "file"
) -> None:
    """
    Validates that a file is within the size limit.
    
    Args:
        file_obj: File bytes or BytesIO object
        max_size_mb: Maximum allowed file size in megabytes
        filename: Name of file for error messages
        
    Raises:
        FileValidationError: If file exceeds size limit
    """
    size_mb = get_file_size_mb(file_obj)
    
    if size_mb > max_size_mb:
        raise FileValidationError(
            f"File '{filename}' is too large ({size_mb:.1f}MB). "
            f"Maximum allowed size is {max_size_mb}MB. "
            f"Try splitting the document or reducing its size."
        )
    
    if size_mb == 0:
        raise FileValidationError(
            f"File '{filename}' is empty (0 bytes). Please upload a valid file."
        )


def validate_file_type(filename: str, allowed_extensions: list = None) -> None:
    """
    Validates that a file has an allowed extension.
    
    Args:
        filename: Name of the file
        allowed_extensions: List of allowed extensions (e.g., ['.pdf', '.txt'])
        
    Raises:
        FileValidationError: If file type is not allowed
    """
    if allowed_extensions is None:
        allowed_extensions = ['.pdf', '.txt']
    
    if not filename or not filename.strip():
        raise FileValidationError("Filename is empty or invalid.")
    
    filename_lower = filename.lower()
    
    # Check extension
    if not any(filename_lower.endswith(ext) for ext in allowed_extensions):
        allowed_str = ', '.join(allowed_extensions)
        raise FileValidationError(
            f"File type not allowed for '{filename}'. "
            f"Allowed types: {allowed_str}. "
            f"Please upload a supported file format."
        )


def validate_pdf_header(file_bytes: bytes) -> bool:
    """
    Validates that a file has a PDF header (basic content-type check).
    
    Args:
        file_bytes: First few bytes of the file
        
    Returns:
        True if file appears to be a PDF
    """
    # PDF files start with %PDF-
    if len(file_bytes) < 5:
        return False
    
    return file_bytes[:4] == b'%PDF' or file_bytes[:5] == b'%PDF-'


def validate_pdf_content(file_obj: Union[bytes, io.BytesIO], filename: str = "PDF") -> None:
    """
    Validates PDF file content (not just extension).
    
    Args:
        file_obj: File bytes or BytesIO object
        filename: Filename for error messages
        
    Raises:
        FileValidationError: If file is not a valid PDF
    """
    # Get first few bytes
    if isinstance(file_obj, bytes):
        header_bytes = file_obj[:10]
    elif isinstance(file_obj, io.BytesIO):
        current_pos = file_obj.tell()
        file_obj.seek(0)
        header_bytes = file_obj.read(10)
        file_obj.seek(current_pos)
    else:
        # Can't validate, skip
        return
    
    if not validate_pdf_header(header_bytes):
        raise FileValidationError(
            f"File '{filename}' does not appear to be a valid PDF. "
            f"The file might be corrupted or have an incorrect extension."
        )


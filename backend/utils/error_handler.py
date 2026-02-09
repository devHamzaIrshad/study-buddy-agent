"""
Centralized error handling system for Study Buddy.
Provides user-friendly error messages and categorization.
"""
from typing import Optional, Dict, Any
from enum import Enum
import traceback


class ErrorCategory(Enum):
    """Categories of errors for better handling."""
    USER_ERROR = "user"  # User input issues (wrong file type, too large, etc.)
    FILE_ERROR = "file"  # File processing issues (corrupted, unreadable, etc.)
    SYSTEM_ERROR = "system"  # System/API issues (out of memory, API down, etc.)
    VALIDATION_ERROR = "validation"  # Data validation failures


class StudyBuddyError(Exception):
    """Base exception for Study Buddy application."""
    
    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.SYSTEM_ERROR,
        user_message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.category = category
        self.user_message = user_message or message
        self.details = details or {}
    
    def get_user_friendly_message(self) -> str:
        """Returns a user-friendly error message with emoji."""
        emoji_map = {
            ErrorCategory.USER_ERROR: "⚠️",
            ErrorCategory.FILE_ERROR: "📄",
            ErrorCategory.SYSTEM_ERROR: "🔧",
            ErrorCategory.VALIDATION_ERROR: "✋"
        }
        emoji = emoji_map.get(self.category, "❌")
        return f"{emoji} {self.user_message}"


class PDFProcessingError(StudyBuddyError):
    """Raised when PDF processing fails."""
    
    def __init__(self, message: str, filename: str = "", page_num: Optional[int] = None):
        details = {"filename": filename}
        if page_num is not None:
            details["page_num"] = page_num
            user_msg = f"Error processing '{filename}' at page {page_num}: {message}"
        else:
            user_msg = f"Error processing '{filename}': {message}"
        
        super().__init__(
            message=message,
            category=ErrorCategory.FILE_ERROR,
            user_message=user_msg,
            details=details
        )


class ChunkingError(StudyBuddyError):
    """Raised when text chunking fails."""
    
    def __init__(self, message: str, doc_name: str = ""):
        super().__init__(
            message=message,
            category=ErrorCategory.SYSTEM_ERROR,
            user_message=f"Failed to process document '{doc_name}': {message}",
            details={"doc_name": doc_name}
        )


def handle_error(error: Exception, context: str = "") -> str:
    """
    Handles errors and returns user-friendly message.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
        
    Returns:
        User-friendly error message string
    """
    # If it's our custom error, use the user-friendly message
    if isinstance(error, StudyBuddyError):
        return error.get_user_friendly_message()
    
    # Handle common Python exceptions
    error_type = type(error).__name__
    error_msg = str(error)
    
    # Map common errors to user-friendly messages
    if "memory" in error_msg.lower() or isinstance(error, MemoryError):
        return "🔧 Out of memory! Try uploading a smaller file or close other applications."
    
    if "permission" in error_msg.lower() or isinstance(error, PermissionError):
        return "🔒 Permission denied. Check file permissions and try again."
    
    if "timeout" in error_msg.lower():
        return "⏱️ Operation timed out. The file might be too large or complex."
    
    if isinstance(error, FileNotFoundError):
        return "📁 File not found. Please try uploading again."
    
    if isinstance(error, ValueError):
        return f"✋ Invalid input: {error_msg}"
    
    # Generic error message with context
    context_str = f" ({context})" if context else ""
    return f"❌ Unexpected error{context_str}: {error_msg}"


def log_error(error: Exception, context: str = ""):
    """
    Logs error details for debugging.
    
    Args:
        error: The exception to log
        context: Additional context
    """
    print(f"\n{'='*60}")
    print(f"ERROR in {context if context else 'application'}")
    print(f"Type: {type(error).__name__}")
    print(f"Message: {str(error)}")
    
    if isinstance(error, StudyBuddyError):
        print(f"Category: {error.category.value}")
        print(f"Details: {error.details}")
    
    print(f"\nTraceback:")
    traceback.print_exc()
    print(f"{'='*60}\n")

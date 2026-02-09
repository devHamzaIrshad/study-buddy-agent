import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.utils.chunking import chunk_text, validate_chunk

class TestChunking(unittest.TestCase):
    def test_chunk_validation(self):
        """Test chunk validation logic."""
        self.assertTrue(validate_chunk("This is a valid chunk with enough content."))
        self.assertFalse(validate_chunk(""))
        self.assertFalse(validate_chunk("   "))
        self.assertFalse(validate_chunk("a")) # Too short
        self.assertFalse(validate_chunk(".......")) # Not enough alphanumeric

    def test_sentence_aware_chunking(self):
        """Test that chunks look reasonable."""
        text = "This is sentence one. This is sentence two. " * 50
        chunks = list(chunk_text(text, chunk_size=100, overlap=20))
        
        self.assertTrue(len(chunks) > 0)
        # Check that chunks are not too large
        for chunk in chunks:
            self.assertTrue(len(chunk) <= 120) # A bit of flexibility for sentence boundaries

if __name__ == "__main__":
    unittest.main()

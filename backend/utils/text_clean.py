import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    # Remove excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
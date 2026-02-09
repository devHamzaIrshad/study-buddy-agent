from backend.utils.text_clean import clean_text

def read_text_bytes(txt_bytes: bytes) -> str:
    try:
        raw = txt_bytes.decode("utf-8", errors="ignore")
    except Exception:
        raw = str(txt_bytes)
    return clean_text(raw)
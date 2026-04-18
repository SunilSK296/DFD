import re

def detect_document_type(text):
    text = text.lower()

    # Aadhaar
    if "aadhaar" in text or "government of india" in text:
        if re.search(r"\d{4}\s\d{4}\s\d{4}", text):
            return "aadhaar"

    # PAN
    if "income tax department" in text or "permanent account number" in text:
        if re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text):
            return "pan"

    # SSLC
    if "marks card" in text or "total" in text:
        return "sslc"

    return "unknown"

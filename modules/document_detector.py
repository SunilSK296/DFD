import re

def detect_document_type(text):
    text = text.lower()

    aadhaar_score = 0
    pan_score = 0
    sslc_score = 0

    # Aadhaar clues
    if "government of india" in text:
        aadhaar_score += 2

    if "dob" in text or "yob" in text:
        aadhaar_score += 1

    if "male" in text or "female" in text:
        aadhaar_score += 1

    if re.search(r"\d{4}", text):  # partial number detection
        aadhaar_score += 1

    # PAN clues
    if "income tax department" in text:
        pan_score += 2

    if re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text):
        pan_score += 2

    # SSLC clues
    if "marks" in text or "total" in text:
        sslc_score += 2

    # Decision
    if aadhaar_score >= 3:
        return "aadhaar"
    elif pan_score >= 2:
        return "pan"
    elif sslc_score >= 2:
        return "sslc"
    else:
        return "unknown"

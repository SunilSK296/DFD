import re

def check_pan(texts):
    score = 0
    reasons = []

    text = " ".join(texts)

    if not re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text):
        score += 30
        reasons.append("Invalid PAN format")

    if "father" not in text.lower():
        score += 10
        reasons.append("Father name missing")

    return score, reasons

import re

def check_aadhaar(texts):
    score = 0
    reasons = []

    text = " ".join(texts)

    if not re.search(r"\d{12}", text):
        score += 30
        reasons.append("Invalid Aadhaar number")

    if "dob" not in text.lower():
        score += 10
        reasons.append("DOB missing")

    if "male" not in text.lower() and "female" not in text.lower():
        score += 10
        reasons.append("Gender field missing")

    return score, reasons

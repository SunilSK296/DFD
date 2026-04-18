import re

def check_sslc(texts):
    score = 0
    reasons = []

    numbers = [int(x) for x in re.findall(r"\d+", " ".join(texts))]

    if len(numbers) < 5:
        score += 20
        reasons.append("Insufficient marks data")

    if "total" not in " ".join(texts).lower():
        score += 10
        reasons.append("Total missing")

    return score, reasons

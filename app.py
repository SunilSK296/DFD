from flask import Flask, request, render_template
import os

app = Flask(__name__)

# HEALTH CHECK (Render needs this to respond quickly)
@app.route("/")
def health():
    return "OK"

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    os.makedirs("uploads", exist_ok=True)
    path = os.path.join("uploads", file.filename)
    file.save(path)

    # IMPORT HEAVY MODULES HERE (lazy load)
    from modules.document_detector import detect_document_type
    from modules.ocr_module import extract_text
    from modules.forgery_checks import perform_ela, detect_regions
    from modules.aadhaar_rules import check_aadhaar
    from modules.pan_rules import check_pan
    from modules.sslc_rules import check_sslc

    texts, _ = extract_text(path, "unknown")
    doc_type = detect_document_type(" ".join(texts))

    texts, _ = extract_text(path, doc_type)

    ela = perform_ela(path)
    regions = detect_regions(ela)

    score, reasons = 0, []

    if len(regions) > 5:
        score += 25
        reasons.append("Multiple image anomalies detected")

    if doc_type == "aadhaar":
        s, r = check_aadhaar(texts)
    elif doc_type == "pan":
        s, r = check_pan(texts)
    elif doc_type == "sslc":
        s, r = check_sslc(texts)
    else:
        s, r = 20, ["Unknown document"]

    score += s
    reasons += r

    status = "LIKELY GENUINE"
    if score > 70:
        status = "SUSPICIOUS"
    elif score > 40:
        status = "NEEDS REVIEW"

    return {
        "doc_type": doc_type,
        "status": status,
        "score": score,
        "reasons": reasons
    }

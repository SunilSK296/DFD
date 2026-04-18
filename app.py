from flask import Flask, render_template, request
import os

# import your modules
from document_detector import detect_document_type
from ocr_module import extract_text
from forgery_checks import perform_ela, detect_regions
from aadhaar_rules import check_aadhaar
from pan_rules import check_pan
from sslc_rules import check_sslc

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template("index.html", result=None)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    # OCR first pass
    texts, _ = extract_text(path, "unknown")
    doc_type = detect_document_type(" ".join(texts))

    # OCR again
    texts, _ = extract_text(path, doc_type)

    # ELA
    ela = perform_ela(path)
    regions = detect_regions(ela)

    score = 0
    reasons = []

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

    if score > 70:
        status = "SUSPICIOUS"
    elif score > 40:
        status = "NEEDS REVIEW"
    else:
        status = "LIKELY GENUINE"

    result = {
        "doc_type": doc_type,
        "status": status,
        "score": score,
        "reasons": reasons
    }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

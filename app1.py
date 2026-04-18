import streamlit as st
import os

# Import your modules
from modules.document_detector import detect_document_type
from modules.ocr_module import extract_text
from modules.forgery_checks import perform_ela, detect_regions
from modules.aadhaar_rules import check_aadhaar
from modules.pan_rules import check_pan
from modules.sslc_rules import check_sslc
from modules.utils import draw_boxes

st.set_page_config(page_title="DocGuard AI", layout="wide")

st.title("🛡️ DocGuard AI - Forgery Detection")
st.write("Upload Aadhaar / PAN / SSLC document")

# Upload
uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

if uploaded_file:

    # Save temp file
    file_path = "temp.jpg"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.image(file_path, caption="Uploaded Document", use_container_width=True)

    with st.spinner("Analyzing..."):

        # Step 1: OCR (initial)
        texts, _ = extract_text(file_path, "unknown")
        doc_type = detect_document_type(" ".join(texts))

        # Step 2: OCR (correct language)
        texts, _ = extract_text(file_path, doc_type)

        # Step 3: ELA
        ela = perform_ela(file_path)
        regions = detect_regions(ela)

        # Step 4: Scoring
        score = 0
        reasons = []

        # Image anomalies
        # --- ELA SCORING FIX ---
        num_regions = len(regions)

        if num_regions > 8:
            score += 25
            reasons.append(f"High number of suspicious regions detected ({num_regions})")

        elif num_regions > 3:
            score += 15
            reasons.append(f"Moderate image inconsistencies detected ({num_regions})")

        elif num_regions > 0:
            score += 5
            reasons.append("Minor compression variations detected")

        else:
            reasons.append("No strong image tampering detected (ELA clean)")

        # Document rules
        if doc_type == "aadhaar":
            s, r = check_aadhaar(texts)
        elif doc_type == "pan":
            s, r = check_pan(texts)
        elif doc_type == "sslc":
            s, r = check_sslc(texts)
        else:
            s, r = 20, ["Unknown document type"]

        score += s
        reasons += r

        # Final status
        if score > 70:
            status = "SUSPICIOUS"
        elif score > 40:
            status = "NEEDS REVIEW"
        else:
            status = "LIKELY GENUINE"

        # Draw suspicious boxes
        annotated_img = draw_boxes(file_path, regions)

    # ---------------- UI ----------------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Annotated Image")
        st.image(annotated_img, use_container_width=True)

    with col2:
        st.subheader("🔥 ELA Map")
        st.image(ela, use_container_width=True)

    st.divider()

    # ---------------- REPORT ----------------

    st.subheader("📋 Explainable Report")

    st.write("Document Type:", doc_type)
    st.write("Status:", status)
    st.write("Confidence Score:", score)

    st.write("### Reasons:")
    for r in reasons:
        st.write("-", r)

    st.write("### Extracted Text:")
    st.write(texts)

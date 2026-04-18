import easyocr

def get_reader(doc_type):
    if doc_type == "aadhaar":
        return easyocr.Reader(['en','hi'], gpu=False)
    elif doc_type == "pan":
        return easyocr.Reader(['en'], gpu=False)
    elif doc_type == "sslc":
        return easyocr.Reader(['en','kn'], gpu=False)
    else:
        return easyocr.Reader(['en'], gpu=False)

def extract_text(image_path, doc_type):
    reader = get_reader(doc_type)
    results = reader.readtext(image_path)

    texts = [r[1] for r in results]
    return texts, results

import easyocr

_reader_cache = {}

def get_reader(langs):
    key = "_".join(langs)
    if key not in _reader_cache:
        _reader_cache[key] = easyocr.Reader(langs, gpu=False)
    return _reader_cache[key]

def extract_text(image_path, doc_type):
    if doc_type == "aadhaar":
        langs = ["en", "hi"]
    elif doc_type == "sslc":
        langs = ["en", "kn"]
    else:
        langs = ["en"]

    reader = get_reader(langs)
    result = reader.readtext(image_path)
    texts = [r[1] for r in result]
    return texts, result

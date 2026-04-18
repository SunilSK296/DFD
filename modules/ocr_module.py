# ocr_module.py

import easyocr

reader_cache = {}

def get_reader(langs):
    key = "_".join(langs)

    if key not in reader_cache:
        reader_cache[key] = easyocr.Reader(langs, gpu=False)

    return reader_cache[key]


def extract_text(image_path, doc_type):

    if doc_type == "aadhaar":
        langs = ['en', 'hi']
    elif doc_type == "pan":
        langs = ['en']
    elif doc_type == "sslc":
        langs = ['en', 'kn']
    else:
        langs = ['en']

    reader = get_reader(langs)

    results = reader.readtext(image_path)

    texts = [r[1] for r in results]

    return texts, results

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance

def perform_ela(image_path):
    original = Image.open(image_path).convert('RGB')
    original.save("temp.jpg", "JPEG", quality=90)

    resaved = Image.open("temp.jpg")
    diff = ImageChops.difference(original, resaved)

    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema]) or 1

    scale = 255.0 / max_diff
    ela = ImageEnhance.Brightness(diff).enhance(scale)

    return ela

def detect_regions(ela_img):
    img = np.array(ela_img)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    _, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = cnts[0] if len(cnts) == 2 else cnts[1]

    valid = [c for c in contours if cv2.contourArea(c) > 120]
    return valid

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def ocr_func(path):
    if path.endswith('.pdf'):
        return ocr_pdf(path)
    else:
        return ocr_image(path)

def ocr_pdf(path):
    images = convert_from_path(path)
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def ocr_image(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)

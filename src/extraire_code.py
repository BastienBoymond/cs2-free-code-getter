import pytesseract
from PIL import Image
import re
import sys
import cv2
import numpy as np
from collections import Counter

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image_path = sys.argv[1] if len(sys.argv) > 1 else 'downloaded_images/DLSTD0_NxNd.jpg'

def extraire_code(image_path):
    """Extrait le code promo de l'image"""
    exclusions = {'PROMOCODE', 'COM', 'CSGOCASES', 'CSGOCASES.COM', 'SKINS', 'FREE', 'CODE', 'CSGOSKINS', 'CSG', 'CS'}
    
    image = Image.open(image_path)
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    preprocessings = {
        'binaire': lambda img: cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1],
        'binaire_inv': lambda img: cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)[1],
        'adaptatif': lambda img: cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15),
        'adaptatif_inv': lambda img: cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 15),
        'otsu': lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        'otsu_inv': lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1],
    }
    
    psm_modes = [6, 7, 11]
    
    all_codes = []
    
    for prep_name, prep_func in preprocessings.items():
        pre_img = prep_func(gray)
        pil_img = Image.fromarray(pre_img)
        for psm in psm_modes:
            config = f'--psm {psm}'
            texte = pytesseract.image_to_string(pil_img, lang='eng', config=config)
            print(f'--- Prétraitement: {prep_name}, PSM: {psm} ---')
            print(texte)
            codes = re.findall(r'\b[A-Z0-9]{3,12}\b', texte)
            codes_filtrés = [c for c in codes if c not in exclusions]
            all_codes.extend(codes_filtrés)

    if all_codes:
        code_counts = Counter(all_codes)
        best_code = sorted(code_counts.items(), key=lambda x: (-x[1], -len(x[0])))[0][0]
        print(f"\nCode le plus probable : {best_code}")
        print(f"Tous les codes candidats : {set(all_codes)}")
        return best_code
    else:
        print("Aucun code trouvé.")
        return None

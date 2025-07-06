import pytesseract
from PIL import Image
import re
import sys
import cv2
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_code(image_path, partie='inférieure'):
    
    
    image = Image.open(image_path)
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    marge = int(gray.shape[1] * 0.15)

    hauteur, largeur = gray.shape
    if partie == 'supérieure':
        gray = gray[:hauteur // 2 , marge:largeur - marge]
        gray = cv2.resize(gray, (largeur // 2, hauteur // 2))
    elif partie == 'inférieure':
        gray = gray[hauteur // 2:, marge:largeur - marge]
        gray = cv2.resize(gray, (0, 0), fx=0.8, fy=0.8)  

    preprocessings = {
        'binaire': lambda img: cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1],
        'otsu': lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        'otsu_inv': lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1],
        'gaussian_blur': lambda img: cv2.GaussianBlur(img, (5, 5), 0)
    }
    
    psm_modes = [3, 6, 11]

    all_codes = []

    for prep_func in preprocessings.values():
        pre_img = prep_func(gray)
        pil_img = Image.fromarray(pre_img)
        for psm in psm_modes:
            config = f'--psm {psm} -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --oem 1'
            texte = pytesseract.image_to_string(pil_img, lang='eng', config=config)
            texte = texte.upper() 
            codes = re.findall(r'\b[A-Z0-9]{3,12}\b', texte)
            all_codes.extend(codes)

    banned_codes = {'FREECDE', 'XYZ789'}  

    print(f"Codes extraits avant filtrage : {all_codes}")

    if all_codes:
        code_counts = Counter(all_codes)
        sorted_codes = sorted(code_counts.items(), key=lambda x: (-x[1], -len(x[0])))
        best_code = None
        second_best_code = None
        for code, _ in sorted_codes:
            if code not in banned_codes:
                if best_code is None:
                    best_code = code
                elif second_best_code is None:
                    second_best_code = code
                    break

        print(f"Codes candidats extraits : {set(all_codes)}")

        print(f"Codes triés : {sorted_codes}")

        print(f"Meilleur code : {best_code}")
        print(f"Deuxième meilleur code : {second_best_code}")

        if 'FREECDE' in [code for code, _ in sorted_codes]:
            print("'FREECDE' trouvé dans la liste, recherche du code avec le plus d'occurrences (excluant FREECDE)...")
            for code, count in sorted_codes:
                if code != 'FREECDE':
                    best_code = code
                    break
        
        if partie == 'supérieure' and 'FREECDE' not in [code for code, _ in sorted_codes]:
            print("Pas de 'FREECDE' trouvé dans la partie supérieure, ce n'est probablement pas une image de code.")
            return None

        if best_code:
            print(f"\nCode le plus probable : {best_code}")
            return best_code
        else:
            print("Aucun code valide trouvé après filtrage.")
    print("Aucun code trouvé.")
    return None

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
image_path = sys.argv[1] if len(sys.argv) > 1 else 'downloaded_images/DLSTD0_NxNd.jpg'

def extraire_code(image_path, partie='inférieure'):
    """Extrait le code promo de l'image, avec option pour traiter seulement la partie supérieure ou inférieure."""
    
    image = Image.open(image_path)
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    # Calculer les marges à enlever
    marge = int(gray.shape[1] * 0.15)

    # Diviser l'image en quarts et sauvegarder les parties
    hauteur, largeur = gray.shape
    if partie == 'supérieure':
        gray = gray[:hauteur // 2 , marge:largeur - marge]
        gray = cv2.resize(gray, (0, 0), fx=0.8, fy=0.8) 
        cv2.imwrite('image_supérieure.png', gray)
    elif partie == 'inférieure':
        gray = gray[hauteur // 2:, marge:largeur - marge]
        gray = cv2.resize(gray, (0, 0), fx=0.8, fy=0.8)  
        cv2.imwrite('image_inférieure.png', gray)
    else:
        # Sauvegarder les deux parties
        cv2.imwrite('image_supérieure.png', gray[:hauteur // 4, marge:largeur - marge])
        cv2.imwrite('image_inférieure.png', gray[3 * hauteur // 4:, marge:largeur - marge])

    preprocessings = {
        'binaire': lambda img: cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1],
        'otsu': lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        'otsu_inv': lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1],
        'gaussian_blur': lambda img: cv2.GaussianBlur(img, (5, 5), 0)
    }
    
    psm_modes = [3, 6, 11]

    all_codes = []

    for prep_name, prep_func in preprocessings.items():
        pre_img = prep_func(gray)
        pil_img = Image.fromarray(pre_img)
        for psm in psm_modes:
            config = f'--psm {psm} -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            texte = pytesseract.image_to_string(pil_img, lang='eng', config=config)
            texte = texte.upper()  # Convertir le texte en majuscules
            print(f'--- Prétraitement: {prep_name}, PSM: {psm} ---')
            print(texte)
            codes = re.findall(r'\b[A-Z0-9]{3,12}\b', texte)
            print(codes)
            all_codes.extend(codes)

    banned_codes = {'FREECDE', 'XYZ789'}  # Exemple de codes interdits

    if all_codes:
        code_counts = Counter(all_codes)
        sorted_codes = sorted(code_counts.items(), key=lambda x: (-x[1], -len(x[0])))
        for code, _ in sorted_codes:
            if code not in banned_codes:
                best_code = code
                break
        else:
            best_code = None

        if best_code:
            print(f"\nCode le plus probable : {best_code}")
            print(f"Tous les codes candidats : {set(all_codes)}")
            return best_code
    
    print("Aucun code trouvé.")
    return None

def traiter_images_dossier():
    """Traite toutes les images du dossier 'downloaded_images' et extrait les codes."""
    dossier_images = 'downloaded_images'
    fichiers_images = [f for f in os.listdir(dossier_images) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    resultats = {}
    for fichier in fichiers_images:
        chemin_image = os.path.join(dossier_images, fichier)
        print(f"Traitement de l'image : {fichier}")
        code = extraire_code(chemin_image, 'supérieure')
        resultats[fichier] = code
    
    print("\nRésultats :")
    for fichier, code in resultats.items():
        print(f"{fichier} : {code}")

# Exemple d'utilisation
if __name__ == "__main__":
    traiter_images_dossier()

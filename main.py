from src.download_image import download_latest_images
from src.extraire_code import traiter_images_dossier
from dotenv import load_dotenv
import os

load_dotenv()


def main():
    """Fonction principale qui combine téléchargement et extraction"""
    print("=== CSGO Cases Code Extractor ===")
    
    print("\n1. Téléchargement des 10 dernières images...")
    download_latest_images()
    
    print("\n2. Extraction des codes promo...")
    traiter_images_dossier()

if __name__ == "__main__":
    main() 
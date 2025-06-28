from src.download_image import download_latest_image
from src.extraire_code import extraire_code
from dotenv import load_dotenv
import os

load_dotenv()


def main():
    """Fonction principale qui combine téléchargement et extraction"""
    print("=== CSGO Cases Code Extractor ===")
    
    print("\n1. Téléchargement de la dernière image...")
    image_path = download_latest_image()
    image_path = "downloaded_images/test.jpg"
    
    if image_path:
        print("\n2. Extraction du code promo...")
        code = extraire_code(image_path)
        
        if code:
            print(f"\n🎉 Code promo trouvé: {code}")
            with open("downloaded_images/latest_code.txt", "w") as f:
                f.write(code)
            print(f"Code sauvegardé dans: downloaded_images/latest_code.txt")
        else:
            print("\n❌ Aucun code promo trouvé dans l'image")

        if image_path and os.path.exists(image_path):
            os.remove(image_path)
            print(f"Image temporaire supprimée: {image_path}")
        else:
            print("Aucune image temporaire à supprimer")
    else:
        print("\n❌ Impossible de télécharger l'image")

if __name__ == "__main__":
    main() 
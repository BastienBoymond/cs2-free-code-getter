from src.download_image import DownloadImage
from src.extraire_code import extract_code
from src.selfbot import Selfbot
import json
from dotenv import load_dotenv
import time

load_dotenv()

def load_setup():
    """Charge les paramètres de configuration"""
    with open('setup.json', 'r') as f:
        return json.load(f)


def main():
    setup = load_setup()
    downloaders = [DownloadImage(site) for site in setup]
    selfbot = Selfbot()
    
    while True:
        for downloader in downloaders:
            images = []
            images.append(downloader.download_instagram_image())
            images.append(downloader.download_facebook_image())
            
            for image in images:
                if image:
                    partie = "supérieure" if image["site"] == "csgoskins" else "inférieure"
                    code = extract_code(image["image_path"], partie)
                    if code:
                        print(f"Code trouvé: {code}")
                        selfbot.send_message(code)
            
            downloader.delete_image()
        time.sleep(3600)  # Pause d'une heure

if __name__ == "__main__":
    main() 
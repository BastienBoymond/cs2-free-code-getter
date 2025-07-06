from src.download_image import DownloadImage
from src.extraire_code import extract_code
from src.selfbot import Selfbot
import json
from dotenv import load_dotenv
import time
import os

load_dotenv()

def load_setup():
    """Charge les paramètres de configuration"""
    with open('setup.json', 'r') as f:
        return json.load(f)


def load_last_codes():
    """Charge les derniers codes enregistrés"""
    if os.path.exists('last_code.json'):
        with open('last_code.json', 'r') as f:
            return json.load(f)
    return []


def save_last_codes(last_codes):
    """Enregistre les derniers codes"""
    with open('last_code.json', 'w') as f:
        json.dump(last_codes, f, indent=4)


def main():
    setup = load_setup()
    last_codes = load_last_codes()
    selfbot = Selfbot()
    downloaders = [DownloadImage(site, selfbot) for site in setup]
    
    while True:
        for downloader in downloaders:
            images = []
            images.append(downloader.download_instagram_image())
            images.append(downloader.download_facebook_image())
            images.append(downloader.download_discord_image())
            
            for image in images:
                if image:
                    partie = "supérieure" if image["site"] == "csgoskins" else "inférieure"
                    code = extract_code(image["image_path"], partie)
                    if code:
                        last_code_entry = next((entry for entry in last_codes if entry['site'] == image['site'] and entry['source'] == image['source']), None)
                        if not last_code_entry or last_code_entry['lastcode'] != code:
                            print(f"Nouveau code trouvé pour {image['source']} sur {image['site']}: {code}")
                            selfbot.send_message(code)
                            if last_code_entry:
                                last_code_entry['lastcode'] = code
                            else:
                                last_codes.append({'site': image['site'], 'source': image['source'], 'lastcode': code})
                        else:
                            print(f"Code déjà envoyé pour {image['source']} sur {image['site']}: {code}")
            
            downloader.delete_image()
        
        save_last_codes(last_codes)
        time.sleep(3600)  # Pause d'une heure

if __name__ == "__main__":
    main() 
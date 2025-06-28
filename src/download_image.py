import os
from dotenv import load_dotenv
from instagrapi import Client
import requests

load_dotenv()

def download_latest_image():
    """Télécharge la dernière image du compte Instagram CSGOCases"""
    cl = Client()
    cl.login(os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))

    user_id = cl.user_id_from_username("csgocasescom")
    medias = cl.user_medias(user_id, 1)

    print("Médias récupérés:")
    print(medias)

    if medias:
        media = medias[0]
        
        if not os.path.exists("downloaded_images"):
            os.makedirs("downloaded_images")
        
        image_url = media.thumbnail_url
        image_filename = f"downloaded_images/{media.code}.jpg"
        
        print(f"\nTéléchargement de l'image: {image_url}")
        response = requests.get(image_url)
        
        if response.status_code == 200:
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            print(f"Image téléchargée: {image_filename}")
         
            return image_filename
        else:
            print(f"Erreur lors du téléchargement: {response.status_code}")
            return None
    else:
        print("Aucun média trouvé")
        return None
import os
from dotenv import load_dotenv
from instagrapi import Client
import requests
import json

load_dotenv()

def download_latest_images():
    """Télécharge les 10 dernières images du compte Instagram CSGOCases"""
    cl = Client()
    
    # Charger les paramètres de session si disponibles
    if os.path.exists('session.json'):
        with open('session.json', 'r') as f:
            print("Chargement des paramètres de session...")
            cl.set_settings(json.load(f))
    else:
        print("Connexion à Instagram...")
        cl.login(os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))
        # Sauvegarder les paramètres de session après la connexion
        with open('session.json', 'w') as f:
            json.dump(cl.get_settings(), f)

    try:
        user_id = cl.user_id_from_username("csgoskins_official")
        medias = cl.user_medias(user_id, 18)  # Récupérer 10 médias
    except Exception as e:
        print("Erreur de session, tentative de reconnexion...")
        cl.login(os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))
        # Sauvegarder les paramètres de session après la reconnexion
        with open('session.json', 'w') as f:
            json.dump(cl.get_settings(), f)
        # Réessayer après la reconnexion
        user_id = cl.user_id_from_username("csgocasescom")
        medias = cl.user_medias(user_id, 10)

    print("Médias récupérés:")
    print(medias)

    if medias:
        if not os.path.exists("downloaded_images"):
            os.makedirs("downloaded_images")
        
        for media in medias:
            image_url = media.thumbnail_url
            image_filename = f"downloaded_images/{media.code}.jpg"
            
            print(f"\nTéléchargement de l'image: {image_url}")
            response = requests.get(image_url)
            
            if response.status_code == 200:
                with open(image_filename, 'wb') as f:
                    f.write(response.content)
                print(f"Image téléchargée: {image_filename}")
            else:
                print(f"Erreur lors du téléchargement: {response.status_code}")
    else:
        print("Aucun média trouvé")
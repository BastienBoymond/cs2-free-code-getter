import os
from dotenv import load_dotenv
from instagrapi import Client
import requests
import json

load_dotenv()


class DownloadImage:
    def __init__(self, site):
        self.site_name = site['site']
        self.username_instagram = site['username_instagram']
        self.username_facebook = site['username_facebook']
        self.discord_channel_id = site['discord_channel_id']
        self.setup_clients()
    
    def setup_clients(self):
        self.cl_instagram = Client()
        
        if os.path.exists('session_instagram.json'):
            with open('session_instagram.json', 'r') as f:
                self.cl_instagram.set_settings(json.load(f))
        else:
            self.cl_instagram.login(os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))
            with open('session_instagram.json', 'w') as f:
                json.dump(self.cl_instagram.get_settings(), f)


    def delete_image(self):
        if os.path.exists("downloaded_images"):
            for file in os.listdir("downloaded_images"):
                os.remove(os.path.join("downloaded_images", file))

    def download_facebook_image(self):
        pass

    def download_instagram_image(self):
 
        user_id = self.cl_instagram.user_id_from_username(self.username_instagram)
        medias = self.cl_instagram.user_medias(user_id, 1)  

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
                    return {
                        'image_path': image_filename,
                        'source': 'instagram',
                        'site': self.site_name
                    }
                else:
                    print(f"Erreur lors du téléchargement: {response.status_code}")
                    return None
        else:
            print("Aucun média trouvé")
            return None
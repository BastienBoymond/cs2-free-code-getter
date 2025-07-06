from dotenv import load_dotenv
import requests
import os

load_dotenv()

class Selfbot:
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.output_channel_id = os.getenv("DISCORD_OUTPUT_CHANNEL_ID")
        self.headers = {
            "Authorization": f"{self.token}",
            "Content-Type": "application/json"
        }
        self.base_url = "https://discord.com/api/v9"
        
        
    def read_last_message(self, channel_id):
        print(f"Recherche du dernier message dans le canal {channel_id}")
        url = f"{self.base_url}/channels/{channel_id}/messages?limit=1"
        print(f"URL: {url}")
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            messages = response.json()
            if 'embeds' in messages[0] and len(messages[0]['embeds']) > 0:
                return messages[0]['embeds'][0]['image']['url']
            elif 'attachments' in messages[0] and len(messages[0]['attachments']) > 0:
                return messages[0]['attachments'][0]['url']
            else:
                print("Aucune image trouvée dans les embeds ou les attachments.")
                return None
        else:
            print(f"Erreur lors de la lecture du message: {response.status_code}")
            return None
    

    def send_message(self, message: str):
        url = f"{self.base_url}/channels/{self.output_channel_id}/messages"
        data = {
            "content": message
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            print(f"Message envoyé avec succès: {message}")
        else:
            print(f"Erreur lors de l'envoi du message: {response.status_code}")



   

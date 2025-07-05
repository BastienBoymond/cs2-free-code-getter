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

    def send_message(self, message: str):
        url = f"https://discord.com/api/v9/channels/{self.output_channel_id}/messages"
        data = {
            "content": message
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            print(f"Message envoyé avec succès: {message}")
        else:
            print(f"Erreur lors de l'envoi du message: {response.status_code}")



   

import requests
from dotenv import load_dotenv
import os

load_dotenv()

class DanelClient:
    def __init__(self, base_url):
        self.base_url = base_url

    
    def get_rankings(self):
        url = f"{self.base_url}/ranking"
        payload = {'aiscore_min': 9}
        header = {"x-api-key": os.getenv("DANELFIN_API_KEY")}

        response = requests.get(url, params=payload, headers=header)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch Danelfin rankings: {response.status_code} - {response.text}")
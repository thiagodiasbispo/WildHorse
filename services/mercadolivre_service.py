import os
import requests
from dotenv import load_dotenv


load_dotenv()

class MercadoLivreService:
    def __init__(self):
        self.base_url = os.getenv("ML_BASE_URL")
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        # Lógica completa de OAuth 2
        # Exemplo básico (ajustar com tokens válidos e fluxo OAuth2 com refresh):
        return os.getenv("ACCESS_TOKEN")

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def get(self, endpoint):
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, json):
        response = requests.post(f"{self.base_url}{endpoint}", headers=self.get_headers(), json=json)
        response.raise_for_status()
        return response.json()

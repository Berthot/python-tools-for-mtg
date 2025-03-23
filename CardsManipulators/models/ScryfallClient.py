import time
from typing import List, Dict

import requests


class ScryfallClient:
    BASE_URL = "https://api.scryfall.com"
    CHUNK_SIZE = 75

    def fetch_cards_by_names(self, names: List[str]) -> Dict[str, Dict]:
        """Busca dados do Scryfall para uma lista de nomes de cartas e retorna um dicionário."""
        all_data = {}
        for i in range(0, len(names), self.CHUNK_SIZE):
            chunk = names[i:i + self.CHUNK_SIZE]
            identifiers = [{"name": name} for name in chunk]
            response = requests.post(f"{self.BASE_URL}/cards/collection", json={"identifiers": identifiers})
            if response.status_code != 200:
                print(f"Erro ao buscar dados do Scryfall: {response.status_code}")
                continue
            data = response.json()
            for card_data in data.get('data', []):
                card_name = card_data.get('name')
                if card_name:
                    all_data[card_name] = card_data
        return all_data

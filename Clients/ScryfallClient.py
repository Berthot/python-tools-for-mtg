from typing import List
import time
import requests

from Entities.Scryfall import Scryfall


class ScryfallClient:
    BASE_URL = "https://api.scryfall.com"
    CHUNK_SIZE = 75  # Tamanho máximo permitido pelo Scryfall por requisição

    def get_cards_by_names(self, cards: List[str]) -> List[Scryfall]:
        """Busca dados do Scryfall para uma lista de nomes de cartas e retorna um dicionário."""
        scryfall_cards: [Scryfall] = []
        for i in range(0, len(cards), self.CHUNK_SIZE):
            cards_names_chunk = cards[i:i + self.CHUNK_SIZE]
            identifiers = [{"name": card} for card in cards_names_chunk]
            response = requests.post(f"{self.BASE_URL}/cards/collection", json={"identifiers": identifiers})
            if response.status_code != 200:
                print(f"Erro ao buscar dados do Scryfall: {response.status_code}")
                continue
            data = response.json()
            for scryfall_card_json in data.get('data', []):
                scryfall_card_name = scryfall_card_json.get('name')
                if scryfall_card_name:
                    try:
                        # card = Scryfall.from_name(scryfall_card_name)
                        card = Scryfall.from_json(scryfall_card_json)
                        scryfall_cards.append(card)
                    except Exception as e:
                        print(f"Erro ao buscar dados do Scryfall: ")
            time.sleep(8)
            print("esperando 8 segundos para captar do scryfall")
        return scryfall_cards

# # Criando uma instância do ScryfallClient
# scryfall_client = ScryfallClient()
#
# # Lista de nomes de cartas para buscar
# card_list = ["Counterspell", "Shock"]
#
# # Buscando os dados das cartas
# fetched_cards = scryfall_client.get_cards_by_names(card_list)
#
# # Exibindo os dados retornados
# for scryfall_card in fetched_cards:
#     print(f"Dados da carta '{scryfall_card.name}':")
#     print(f"  Tipo: {scryfall_card.type_line}")
#     print(f"  Texto Oracle: {scryfall_card.oracle_text}")
#     print("-" * 40)

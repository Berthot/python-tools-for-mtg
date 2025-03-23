from dataclasses import asdict, is_dataclass
from typing import List, Optional, Dict
import msgpack
import os

class CardRepository:
    def __init__(self, file_path: str = "cards.msgpack"):
        self.file_path = file_path
        self.cards = self._load_cards()

    def _load_cards(self) -> List[Dict]:
        """Carrega as cartas do arquivo MessagePack."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "rb") as file:
                return msgpack.unpackb(file.read(), raw=False)
        return []

    def _save_cards(self):
        """Salva as cartas no arquivo MessagePack."""
        with open(self.file_path, "wb") as file:
            file.write(msgpack.packb(self.cards, use_bin_type=True))

    def add_card(self, card):
        """Adiciona uma nova carta ao armazenamento."""
        card_dict = self._card_to_dict(card)
        self.cards.append(card_dict)
        self._save_cards()

    def get_card_by_name(self, name: str) -> Optional[Dict]:
        """Busca uma carta pelo nome."""
        for card_dict in self.cards:
            if card_dict.get("name") == name:
                return card_dict
        return None

    def get_all_cards(self) -> List[Dict]:
        """Retorna todas as cartas armazenadas."""
        return self.cards

    def _card_to_dict(self, card) -> Dict:
        """Converte um objeto Card ou ScryfallCard em um dicionário."""
        if is_dataclass(card):
            return asdict(card)
        raise ValueError("O objeto não é uma dataclass.")

    def _dict_to_card(self, card_dict: Dict, card_class):
        """Converte um dicionário de volta para um objeto Card ou ScryfallCard."""
        return card_class(**card_dict)
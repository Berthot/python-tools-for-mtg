import re
from dataclasses import dataclass, field
from typing import Optional, List

from Entities.Card import Card


@dataclass
class Deck:
    cards: List[Card] = field(default_factory=list)
    scryfall_fetched: bool = False

    def __init__(self, file_path: Optional[str] = None):
        self.cards = []
        self.not_found_cards = []
        if file_path:
            self.load_from_file(file_path)

    def add_card(self, card: Card):
        self.cards.append(card)



    def load_from_file(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    card = self.parse_card_line(line)
                    self.add_card(card)

    def get_not_found_cards(self) -> List[Card]:
        if not self.scryfall_fetched:
            return []
        if not self.not_found_cards:
            self.not_found_cards = [card for card in self.cards if not card.has_scryfall]
        return self.not_found_cards

    @staticmethod
    def parse_card_line(line: str) -> Card:
        pattern = re.compile(
            r'(?P<quantity>\d+)x?\s+(?P<name>[^(^\[]+)'
            r'(?:\((?P<collection>[^)]+)\))?'
            r'(?:\s\d+|\s\*F\*)?'
            r'(?:\s?\[(?P<category>[^]]+)])?'
            r'(?:\s?\^(?P<color_tag>[^\^]+)\^)?'
        )
        match = pattern.match(line.strip())
        if match:
            card_json = match.groupdict()
            return Card().from_dict(card_json)

        else:
            raise ValueError(f"Formato da linha não reconhecido: {line}")

    @staticmethod
    def get_primary_name(card_name: str) -> str:
        return card_name.split('//')[0].strip()

    def print_deck_list(self):
        if not self.scryfall_fetched:
            print("Deck List:")
            for card in self.cards:
                print(card)
            return

        found_cards = [card for card in self.cards if card.has_scryfall]
        not_found_cards = [card for card in self.cards if not card.has_scryfall]

        if found_cards:
            print("Deck List:")
            for card in found_cards:
                print(card)
        if not_found_cards:
            print("\nNOT_FOUND:")
            for card in not_found_cards:
                print(card)

import re
from dataclasses import dataclass, field
from typing import Optional, List

from CardsManipulators.models.Card import Card
from CardsManipulators.models.ScryfallCard import ScryfallCard
from CardsManipulators.models.ScryfallClient import ScryfallClient


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

    def update_color_tag_from_deck(self, other_deck: 'Deck'):
        color_tag_map = {card.name: card.color_tag for card in other_deck.cards if card.color_tag}
        for card in self.cards:
            if card.name in color_tag_map:
                card.color_tag = color_tag_map[card.name]

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
            self.not_found_cards = [card for card in self.cards if not card.found_in_scryfall]
        return self.not_found_cards

    def fetch_all_scryfall_data(self):
        client = ScryfallClient()
        primary_names = [card.get_primary_name() for card in self.cards]
        scryfall_data = client.fetch_cards_by_names(primary_names)

        for card in self.cards:
            card_data = scryfall_data.get(card.name)
            if card_data:
                scryfall_card = ScryfallCard(deck_category=card.category, name=card.name)
                scryfall_card.from_scryfall_data(card_data)
                card.scryfall_card = scryfall_card
                card.found_in_scryfall = True
            else:
                card.found_in_scryfall = False
        self.scryfall_fetched = True

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
            card_info = match.groupdict()
            return Card(
                name=card_info['name'].strip(),
                collection=card_info.get('collection'),
                quantity=int(card_info['quantity']) if card_info.get('quantity') else None,
                category=card_info.get('category'),
                color_tag=card_info.get('color_tag')
            )
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

        found_cards = [card for card in self.cards if card.found_in_scryfall]
        not_found_cards = [card for card in self.cards if not card.found_in_scryfall]

        if found_cards:
            print("Deck List:")
            for card in found_cards:
                print(card)
        if not_found_cards:
            print("\nNOT_FOUND:")
            for card in not_found_cards:
                print(card)

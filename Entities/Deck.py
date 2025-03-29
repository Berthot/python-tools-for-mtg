import json
import re
from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID

from Entities.Card import Card
from Entities.enums.EExportFormat import EExportFormat


@dataclass
class Deck:
    cards: List[Card] = field(default_factory=list)
    scryfall_fetched: bool = False
    _base_path: str = 'Files'
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
                if line.strip() == '':
                    continue
                if line.strip():
                    card = self.parse_card_line(line)
                    self.add_card(card)

    def get_not_found_cards(self) -> List[Card]:
        if not self.scryfall_fetched:
            return []
        if not self.not_found_cards:
            self.not_found_cards = [card for card in self.cards if not card.has_scryfall]
        return self.not_found_cards

    def export(self, format: EExportFormat = EExportFormat.JSON, full: bool = False) -> str:
        """
        Exporta o deck como JSON ou como texto (formato Archidekt-like).

        Args:
            format (str): 'json' ou 'archidekt'
            full (bool): Se true, exporta dados completos (para JSON)

        Returns:
            str: Representação exportada do deck
        """

        def default_serializer(obj):
            if isinstance(obj, UUID):
                return str(obj)
            raise TypeError(f"Type {type(obj)} not serializable")

        if format == EExportFormat.JSON:
            self._export_as_json(default_serializer, full)
        elif format == EExportFormat.ARCHIDEKT:
            self._export_as_archidekt()
        else:
            raise ValueError("Formato de exportação inválido. Use 'json' ou 'archidekt'.")

    def _export_as_archidekt(self):
        path = f'{self._base_path}/archidekt.txt'
        print("\n📤 Exportando como Archidekt...")
        cards_dict = [card.to_deck_archidekt_line() + '\n' for card in self.cards]
        with open(path, 'w', encoding='utf-8') as txt_file:
            for card in cards_dict:
                txt_file.writelines(card)
        print(f"📤 Exportado _> {path}")


    def _export_as_json(self, default_serializer, full):
        path = f"{self._base_path}/deck_list.json"
        print("\n📤 Exportando como JSON...")
        cards_dict = [card.export_as_dict(full) for card in self.cards]
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(cards_dict, json_file, default=default_serializer, indent=4, ensure_ascii=False)
        print(f"📤 Exportado _> {path}")

    @staticmethod
    def parse_card_line(line: str) -> 'Card':
        line = line.strip()

        # Extrai quantidade
        quantity_match = re.match(r'^(\d+)x?\s+', line)
        if not quantity_match:
            raise ValueError(f"Invalid quantity in line: {line}")

        quantity = int(quantity_match.group(1))
        remaining = line[quantity_match.end():]

        # Extrai tag de cor (se existir)
        color_tag = None
        if '^' in remaining:
            remaining, color_part = remaining.rsplit('^', 1)
            color_tag_match = re.search(r'\^([^^]+)\^$', remaining + '^' + color_part)
            if color_tag_match:
                color_tag = color_tag_match.group(1)
                remaining = remaining.replace(f'^{color_tag}^', '')

        # Extrai categoria (se existir)
        deck_category = None
        if '[' in remaining:
            remaining, category_part = remaining.rsplit('[', 1)
            category_match = re.search(r'\[([^\]]+)\]$', '[' + category_part)
            if category_match:
                # Split por vírgula e remover espaços em branco
                categories = [cat.strip() for cat in category_match.group(1).split(',')]
                deck_category = categories if len(categories) > 1 else category_match.group(1)

        # Extrai coleção e número do coletor (se existirem)
        collection = None
        collector_number = None
        if '(' in remaining:
            collection_match = re.search(r'\(([^)]+)\)', remaining)
            if collection_match:
                collection_info = collection_match.group(1).split()
                collection = collection_info[0]
                if len(collection_info) > 1:
                    collector_number = collection_info[1]
                remaining = remaining.replace(f'({collection_match.group(1)})', '')

        # O que sobrou é o nome da carta
        name = remaining.strip()
        if "elves" in name:
            pass
        if "Elves" in name:
            pass

        return Card(
            name=name,
            collection=collection,
            quantity=quantity,
            deck_category=deck_category,
            color_tag=color_tag
        )

    @staticmethod
    def get_primary_name(card_name: str) -> str:
        if "//" not in card_name:
            return card_name
        return card_name.split('//')[0].strip()

    def print(self):
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

import json
import re
from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID

from Configurations.EnvManager import EnvManager
from Entities.Card import Card
from Entities.enums.EExportFormat import EExportFormat


@dataclass
class Deck:
    cards: List[Card] = field(default_factory=list)
    scryfall_fetched: bool = False
    _export_base_path: str = 'Files'

    def __init__(self, base_path: Optional[str] = None, file_name: Optional[str] = None, use_generic_name: bool = False):
        self._use_generic_name = use_generic_name
        env_manager = EnvManager()
        env_default_export_base_path = env_manager.get_env(env_name='DEFAULT_EXPORT_BASE_PATH')
        env_default_export_file_name = env_manager.get_env(env_name='DEFAULT_EXPORT_FILE_NAME')
        env_default_import_file_name = env_manager.get_env(env_name='DEFAULT_IMPORT_FILE_NAME')
        self.cards = []
        self.not_found_cards = []
        self._export_base_path = str(env_default_export_base_path) if base_path is None else base_path
        self._export_default_file_name = str(env_default_export_file_name)
        self._import_file_name = str(env_default_import_file_name) if file_name is None else file_name

        if file_name:
            self.load_from_file()

    def add_card(self, card: Card):
        self.cards.append(card)

    def load_from_file(self):
        with open(f'./Files/{self._import_file_name}.txt', 'r', encoding='utf-8') as file:
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

    def export(self, export_format: EExportFormat = EExportFormat.JSON, full: bool = False,
               internal_export=False) -> str:
        """
        Exporta o deck como JSON ou como texto (formato Archidekt-like).

        Args:
            format (str): 'json' ou 'archidekt'
            full (bool): Se true, exporta dados completos (para JSON)

        Returns:
            str: Representação exportada do deck
            :param internal_export:
            :param full:
            :param export_format:
        """

        def default_serializer(obj):
            if isinstance(obj, UUID):
                return str(obj)
            raise TypeError(f"Type {type(obj)} not serializable")

        if export_format == EExportFormat.JSON:
            self._export_as_json(default_serializer, full, internal_export=internal_export)
        elif export_format == EExportFormat.ARCHIDEKT:
            self._export_as_archidekt(internal_export=internal_export)
        elif export_format == EExportFormat.LIGA:
            self._export_as_liga(internal_export=internal_export)
        else:
            raise ValueError("Formato de exportação inválido. Use 'json' ou 'archidekt'.")

    def file_name_or_default(self):
        if self._use_generic_name:
            return self._export_default_file_name
        return self._export_default_file_name if self.find_commander() is None else self.find_commander()

    def find_commander(self):
        for card in self.cards:
            if card.deck_category:
                # Se for string, verifica se contém 'Commander'
                if isinstance(card.deck_category, str) and 'Commander' in card.deck_category:
                    return card.normalize_filename()
                # Se for lista, verifica se algum item contém 'Commander'
                elif isinstance(card.deck_category, list) and any(
                        'Commander' in category for category in card.deck_category):
                    return card.normalize_filename()
        return None


    def _export_as_liga(self, internal_export=False):
        file_name = self.file_name_or_default()
        path = f'{self._export_base_path}/LIGA_{file_name}.txt'
        if internal_export:
            path = f'Files/LIGA_{file_name}.txt'
        print("\n📤 Exportando como Archidekt...")
        cards_dict = [card.to_deck_liga_line() + '\n' for card in self.cards]
        with open(path, 'w', encoding='utf-8') as txt_file:
            for card in cards_dict:
                txt_file.writelines(card)
        print(f"📤 Exportado _> {path}")

    def _export_as_archidekt(self, internal_export=False):
        file_name = self.file_name_or_default()
        path = f'{self._export_base_path}/ARCHIDEKT_{file_name}.txt'
        if internal_export:
            path = f'Files/ARCHIDEKT_{file_name}.txt'
        print("\n📤 Exportando como Archidekt...")
        cards_dict = [card.to_deck_archidekt_line() + '\n' for card in self.cards]
        with open(path, 'w', encoding='utf-8') as txt_file:
            for card in cards_dict:
                txt_file.writelines(card)
        print(f"📤 Exportado _> {path}")

    def _export_as_json(self, default_serializer, full, internal_export=False):
        file_name = self.file_name_or_default()
        path = f"{self._export_base_path}/{file_name}.json"
        if internal_export:
            path = f'Files/{file_name}.json'
        print("\n📤 Exportando como JSON...")
        cards_dict = [card.export_as_dict(full) for card in self.cards]
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(cards_dict, json_file, default=default_serializer, indent=4, ensure_ascii=False)
        print(f"📤 Exportado _> {path}")

    @staticmethod
    def get_primary_name(card_name: str) -> str:
        if "//" not in card_name:
            return card_name
        return card_name.split('//')[0].strip()

    def print(self, show: bool = False):
        if not show:
            return
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

    def parse_card_line(self, line: str) -> Card:
        line = line.strip()

        # Extrai quantidade
        quantity_match = re.match(r'^(\d+)x?\s+', line)
        if not quantity_match:
            raise ValueError(f"Formato de quantidade inválido: {line}")

        quantity = int(quantity_match.group(1))
        remaining = line[quantity_match.end():]

        # Dicionário para armazenar componentes extraídos
        components = {
            'color_tag': None,
            'color_code': None,
            'deck_category': None,
            'foil': False,
            'collection': None,
            'collector_number': None
        }

        # Ordem de processamento dos componentes (ajustar conforme necessidade)
        processing_order = [
            ('color', r'\^([^^]+)\^', self._process_color),
            ('category', r'\[([^]]+)\]', self._process_category),
            ('foil', r'\*([^*]+)\*', self._process_foil),
            ('collection', r'\(([^)]+)\)', self._process_collection)
        ]

        # Processa cada componente na ordem definida
        for comp_name, pattern, processor in processing_order:
            match = re.search(pattern, remaining)
            if match:
                processor(match, components, remaining)
                remaining = re.sub(pattern, '', remaining, count=1).strip()

        # Restante é o nome da carta
        name = remaining.strip().split('  ')[0].strip()

        card = Card.from_name(name.lower())
        card.quantity = quantity
        card.deck_category = components.get('deck_category')
        card.color_tag = components.get('color_tag')
        card.color_code = components.get('color_code')
        card.foil = components.get('foil')
        card.collection = components.get('collection')
        card.collector_number = components.get('collector_number')
        return card

    # Funções auxiliares para processamento
    @staticmethod
    def _process_color(match, components, remaining):
        color_info = match.group(1).split(',')
        components['color_tag'] = color_info[0]
        if len(color_info) > 1:
            components['color_code'] = color_info[1]

    @staticmethod
    def _process_category(match, components, remaining):
        categories = [cat.strip() for cat in match.group(1).split(',')]
        components['deck_category'] = categories if len(categories) > 1 else match.group(1)

    @staticmethod
    def _process_foil(match, components, remaining):
        components['foil'] = match.group(1).lower() == 'f'

    @staticmethod
    def _process_collection(match, components, remaining):
        collection_info = match.group(1).split()
        components['collection'] = collection_info[0]
        if len(collection_info) > 1:
            components['collector_number'] = ' '.join(collection_info[1:])


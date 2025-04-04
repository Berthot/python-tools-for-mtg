import json
import re
import uuid
from dataclasses import field, dataclass, asdict
from typing import Optional, Dict, List

import unicodedata

from Entities.Scryfall import Scryfall


@dataclass
class Card:
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    name: str = None
    collection: Optional[str] = None
    quantity: Optional[int] = None
    deck_category: Optional[List[str]] = None
    color_tag: Optional[str] = None
    scryfall: Scryfall = None
    has_scryfall: bool = scryfall is not None
    color_code: Optional[str] = None
    foil: Optional[str] = None
    collector_number: Optional[str] = None

    def has_scryfall(self):
        return self.scryfall is not None

    @classmethod
    def from_name(cls, name: str):
        return Card(
            name=name.strip(),
            collection=None,
            quantity=1,
            color_tag=None
        )

    @classmethod
    def from_dict(cls, json: Dict):
        return Card(
            name=json['name'].strip().lower(),
            collection=json.get('collection'),
            quantity=int(json['quantity']) if json.get('quantity') else None,
            deck_category=json.get('category') if isinstance(json.get('category'), list) else [json.get('category')],
            color_tag=json.get('color_tag'),
        )

    def to_deck_liga_line(self) -> str:
        parts = [f"{self.quantity or 1} {self.get_primary_name()}"]

        if self.collection:
            parts.append(f"[{self.collection}]")

        if self.deck_category:
            if 'commander{top}' in self.category_normalized():
                return ''

        return ' '.join(parts)


    def category_normalized(self) -> str:
        if self.deck_category is not None:
            data = ', '.join(self.deck_category) if isinstance(self.deck_category, list) else self.deck_category
            return data
        return ''

    def to_deck_archidekt_line(self) -> str:
        parts = [f"{self.quantity or 1}x {self.name}"]

        if self.collection:
            parts.append(f"({self.collection})")
            parts.append(f"{self.collector_number}")
        if self.deck_category:
            parts.append(f"[{self.category_normalized().split(',')[0]}]")
        if self.color_tag:
            parts.append(f"^{self.color_tag},{self.color_code}^")

        return ' '.join(parts)

    def normalize_filename(self) -> str:
        """
        Normaliza o nome do commander para usar como nome de arquivo:
        - Remove acentos e caracteres especiais
        - Substitui espaços por underscores
        - Remove caracteres não alfanuméricos
        - Converte para lowercase
        """
        # Remove acentos
        name = unicodedata.normalize('NFKD', self.name).encode('ASCII', 'ignore').decode('ASCII')

        # Substitui espaços por underscore
        name = name.replace(' ', '_')

        # Remove caracteres não alfanuméricos (exceto underscore)
        name = re.sub(r'[^\w_]', '', name)

        # Converte para lowercase
        name = name.lower()

        return name

    def export_as_dict(self, full: bool = False):
        if full:
            return self._to_full_json()

        return self._to_simple_dict()

    def _to_simple_dict(self) -> dict:

        simple_dict = {
            "quantity": self.quantity or 1,
            "name": self.scryfall.name if self.scryfall.name else self.name,
            "deck_category": self.deck_category if self.deck_category else None,
            "mana_cost": self.scryfall.mana_cost if self.scryfall else None,
            "cmc": self.scryfall.cmc if self.scryfall else None,
            "card_type": self.scryfall.type_line if self.scryfall else None,
            "card_description": self.scryfall.oracle_text if self.scryfall else None
        }
        if self.color_tag is not None:
            simple_dict['i_have'] = self.color_tag

        if not self.has_scryfall:
            return simple_dict

        is_two_faces = self.scryfall.layout in ['transform', 'split', 'modal_dfc'] and hasattr(self.scryfall, 'card_faces')

        if self.has_scryfall is True and is_two_faces:
            simple_dict[
                "mana_cost"] = f"{self.scryfall.card_faces[0]["mana_cost"]} // {self.scryfall.card_faces[1]["mana_cost"]}"
            simple_dict[
                "card_type"] = f"{self.scryfall.card_faces[0]["type_line"]} // {self.scryfall.card_faces[1]["type_line"]}"
            simple_dict[f"card_description"] = {
                f"{self.scryfall.name.split(' // ')[0]}": f"{self.scryfall.card_faces[0]["oracle_text"]}",
                f"{self.scryfall.name.split(' // ')[1]}": f"{self.scryfall.card_faces[1]["oracle_text"]}",
            }


        return simple_dict

    def _to_full_json(self) -> dict:
        def default_serializer(obj):
            if isinstance(obj, uuid.UUID):
                return str(obj)
            raise TypeError(f"Type {type(obj)} not serializable")

        card_dict = asdict(self)

        # Se tiver um objeto scryfall, exporta também como dict
        if self.scryfall:
            card_dict['scryfall'] = asdict(self.scryfall)

        return card_dict

    def get_primary_name(self) -> str:
        if "//" not in self.name.lower():
            return self.name.lower()
        return self.name.split('//')[0].strip().lower()

    def __str__(self):
        return self.to_deck_archidekt_line()

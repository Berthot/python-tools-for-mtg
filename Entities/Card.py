import json
import uuid
from dataclasses import field, dataclass, asdict
from typing import Optional, Dict

from Entities.Scryfall import Scryfall


@dataclass
class Card:
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    name: str = None
    collection: Optional[str] = None
    quantity: Optional[int] = None
    deck_category: Optional[str] = ""
    color_tag: Optional[str] = None
    scryfall: Optional[Scryfall] = None
    has_scryfall: bool = scryfall is not None

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
            name=json['name'].strip(),
            collection=json.get('collection'),
            quantity=int(json['quantity']) if json.get('quantity') else None,
            deck_category=json.get('category'),
            color_tag=json.get('color_tag'),
        )

    def to_deck_archidekt_line(self) -> str:
        parts = [f"{self.quantity or 1}x {self.name}"]

        if self.collection:
            parts[-1] += f" ({self.collection})"

        if self.deck_category:
            parts.append(f"[{self.deck_category}]")

        if self.color_tag:
            parts.append(f"^{self.color_tag}^")

        return ' '.join(parts)

    def export_as_dict(self, full:bool = False):
        if full:
            return self._to_full_json()

        return self._to_simple_dict()

    def _to_simple_dict(self) -> dict:
        return {
            "quantity": self.quantity or 1,
            "name": self.name,
            "deck_category": self.deck_category,
            "mana_cost": self.scryfall.mana_cost if self.scryfall else None,
            "cmc": int(self.scryfall.cmc if self.scryfall else None),
            "card_type": self.scryfall.type_line if self.scryfall else None,
            "card_description": self.scryfall.oracle_text if self.scryfall else None
        }

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
        return self.name.split('//')[0].strip()

    def __str__(self):
        return self.to_deck_archidekt_line()

import uuid
from dataclasses import field, dataclass
from typing import Optional, Dict

from Entities.Scryfall import Scryfall


@dataclass
class Card:
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    name: str = None
    collection: Optional[str] = None
    quantity: Optional[int] = None
    deck_category: Optional[str] = None
    color_tag: Optional[str] = None
    scryfall: Optional[Scryfall] = None
    has_scryfall: bool = scryfall is not None

    @classmethod
    def from_name(cls, name: str):
        return Card(
            name=name.strip(),
            collection=None,
            quantity=1,
            deck_category=None,
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

    def get_primary_name(self) -> str:
        return self.name.split('//')[0].strip()

    def __str__(self):
        return f"{self.quantity}x {self.name}"

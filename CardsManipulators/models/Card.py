import uuid
from dataclasses import dataclass, field
from typing import Optional

from CardsManipulators.models import ScryfallCard


@dataclass
class Card:
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    name: str
    collection: Optional[str] = None
    quantity: Optional[int] = 1
    category: Optional[str] = None
    color_tag: Optional[str] = None
    scryfall_card: Optional[ScryfallCard] = None
    found_in_scryfall: bool = False

    def get_primary_name(self) -> str:
        return self.name.split('//')[0].strip()

    def __str__(self):
        return f"{self.quantity}x {self.name}"
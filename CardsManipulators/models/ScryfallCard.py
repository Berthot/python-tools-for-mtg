from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class ScryfallCard:
    deck_category: Optional[str] = None
    quantity: Optional[int] = None
    name: Optional[str] = None
    mana_cost: Optional[str] = None
    cmc: Optional[float] = None
    type_line: Optional[str] = None
    oracle_text: Optional[str] = None
    card_faces: Optional[List[Dict]] = None

    def from_scryfall_data(self, data: Dict):
        self.mana_cost = data.get("mana_cost")
        self.cmc = data.get("cmc")
        self.type_line = data.get("type_line")
        self.oracle_text = data.get("oracle_text")
        self.card_faces = data.get("card_faces")

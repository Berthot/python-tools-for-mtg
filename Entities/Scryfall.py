from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class Scryfall:
    name: Optional[str] = None
    quantity: Optional[int] = None
    mana_cost: Optional[str] = None
    cmc: Optional[str] = None
    type_line: Optional[str] = None
    oracle_text: Optional[str] = None
    card_faces: Optional[List[Dict]] = None
    layout: Optional[str] = None
    object: Optional[str] = None
    id: Optional[str] = None
    oracle_id: Optional[str] = None
    multiverse_ids: List[int] = field(default_factory=list)
    mtgo_id: Optional[int] = None
    tcgplayer_id: Optional[int] = None
    cardmarket_id: Optional[int] = None
    lang: Optional[str] = None
    released_at: Optional[str] = None
    uri: Optional[str] = None
    scryfall_uri: Optional[str] = None
    highres_image: bool = False
    image_status: Optional[str] = None
    image_uris: Dict[str, str] = field(default_factory=dict)
    power: Optional[str] = None
    toughness: Optional[str] = None
    colors: List[str] = field(default_factory=list)
    color_identity: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    all_parts: List[Dict[str, str]] = field(default_factory=list)
    legalities: Dict[str, str] = field(default_factory=dict)
    games: List[str] = field(default_factory=list)
    reserved: bool = False
    foil: bool = False
    nonfoil: bool = False
    finishes: List[str] = field(default_factory=list)
    oversized: bool = False
    promo: bool = False
    reprint: bool = False
    variation: bool = False
    set_id: Optional[str] = None
    set: Optional[str] = None
    set_name: Optional[str] = None
    set_type: Optional[str] = None
    set_uri: Optional[str] = None
    set_search_uri: Optional[str] = None
    scryfall_set_uri: Optional[str] = None
    rulings_uri: Optional[str] = None
    prints_search_uri: Optional[str] = None
    collector_number: Optional[str] = None
    digital: bool = False
    rarity: Optional[str] = None
    watermark: Optional[str] = None
    card_back_id: Optional[str] = None
    artist: Optional[str] = None
    artist_ids: List[str] = field(default_factory=list)
    illustration_id: Optional[str] = None
    border_color: Optional[str] = None
    frame: Optional[str] = None
    frame_effects: List[str] = field(default_factory=list)
    security_stamp: Optional[str] = None
    full_art: bool = False
    textless: bool = False
    booster: bool = False
    story_spotlight: bool = False
    edhrec_rank: Optional[int] = None
    preview: Dict[str, str] = field(default_factory=dict)
    prices: Dict[str, Optional[str]] = field(default_factory=dict)
    related_uris: Dict[str, str] = field(default_factory=dict)
    purchase_uris: Dict[str, str] = field(default_factory=dict)

    def __str__(self):
        return f"ScryFallç.Name: {self.name}"

    @classmethod
    def from_name(cls, name: str):
        """ Preenche apenas o campo nome. """
        scryfall = cls()
        scryfall.name = name
        return scryfall

    @classmethod
    def from_json(cls, json: Dict):
        """ Preenche todos os campos da classe com base nos dados da API. """
        scryfall = cls()
        scryfall.advanced_scryfall_data(json)
        return scryfall

    def get_primary_name(self) -> str:
        if "//" not in self.name.lower():
            return self.name.lower()
        return self.name.split('//')[0].strip().lower()

    def advanced_scryfall_data(self, data):
        """Preenche todos os campos da classe com base nos dados da API."""
        self.name = data.get("name").lower()
        self.object = data.get("object")
        self.id = data.get("id")
        self.layout = data.get("layout")
        self.card_faces = data.get("card_faces")
        self.oracle_id = data.get("oracle_id")
        self.multiverse_ids = data.get("multiverse_ids", [])
        self.mtgo_id = data.get("mtgo_id")
        self.tcgplayer_id = data.get("tcgplayer_id")
        self.cardmarket_id = data.get("cardmarket_id")
        self.lang = data.get("lang")
        self.released_at = data.get("released_at")
        self.uri = data.get("uri")
        self.scryfall_uri = data.get("scryfall_uri")
        self.highres_image = data.get("highres_image", False)
        self.image_status = data.get("image_status")
        self.image_uris = data.get("image_uris", {})
        self.mana_cost = data.get("mana_cost")
        self.cmc = data.get("cmc")
        self.type_line = data.get("type_line")
        self.oracle_text = data.get("oracle_text")
        self.power = data.get("power")
        self.toughness = data.get("toughness")
        self.colors = data.get("colors", [])
        self.color_identity = data.get("color_identity", [])
        self.keywords = data.get("keywords", [])
        self.all_parts = data.get("all_parts", [])
        self.legalities = data.get("legalities", {})
        self.games = data.get("games", [])
        self.reserved = data.get("reserved", False)
        self.foil = data.get("foil", False)
        # self.nonfoil = data.get("nonfoil", False)
        self.finishes = data.get("finishes", [])
        # self.oversized = data.get("oversized", False)
        # self.promo = data.get("promo", False)
        self.reprint = data.get("reprint")
        self.variation = data.get("variation")
        self.set_id = data.get("set_id")
        self.set = data.get("set")
        self.set_name = data.get("set_name")
        self.set_type = data.get("set_type")
        self.set_uri = data.get("set_uri")
        self.set_search_uri = data.get("set_search_uri")
        self.scryfall_set_uri = data.get("scryfall_set_uri")
        self.rulings_uri = data.get("rulings_uri")
        self.prints_search_uri = data.get("prints_search_uri")
        self.collector_number = data.get("collector_number")
        # self.digital = data.get("digital", False)
        self.rarity = data.get("rarity")
        self.watermark = data.get("watermark")
        self.card_back_id = data.get("card_back_id")
        self.artist = data.get("artist")
        self.artist_ids = data.get("artist_ids", [])
        self.illustration_id = data.get("illustration_id")
        self.border_color = data.get("border_color")
        self.frame = data.get("frame")
        self.security_stamp = data.get("security_stamp")
        # self.full_art = data.get("full_art", False)
        # self.textless = data.get("textless", False)
        # self.booster = data.get("booster", False)
        # self.story_spotlight = data.get("story_spotlight", False)
        self.edhrec_rank = data.get("edhrec_rank")
        self.preview = data.get("preview", {})
        self.prices = data.get("prices", {})
        # self.related_uris = data.get("related_uris", {})
        # self.purchase_uris = data.get("purchase_uris", {})

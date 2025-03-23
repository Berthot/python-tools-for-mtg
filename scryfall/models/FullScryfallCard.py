import requests
from typing import List, Dict, Optional

class FullScryfallCard:
    def __init__(self, name: str, card_deck_category: str):
        self.deck_category = card_deck_category
        self.quantity = None
        self.name = name
        self.object = None
        self.id = None
        self.oracle_id = None
        self.multiverse_ids = []
        self.mtgo_id = None
        self.tcgplayer_id = None
        self.cardmarket_id = None
        self.lang = None
        self.released_at = None
        self.uri = None
        self.scryfall_uri = None
        self.layout = None
        self.highres_image = False
        self.image_status = None
        self.image_uris = {}
        self.mana_cost = None
        self.cmc = None
        self.type_line = None
        self.oracle_text = None
        self.power = None
        self.toughness = None
        self.colors = []
        self.color_identity = []
        self.keywords = []
        self.all_parts = []
        self.legalities = {}
        self.games = []
        self.reserved = False
        self.foil = False
        self.nonfoil = False
        self.finishes = []
        self.oversized = False
        self.promo = False
        self.reprint = False
        self.variation = False
        self.set_id = None
        self.set = None
        self.set_name = None
        self.set_type = None
        self.set_uri = None
        self.set_search_uri = None
        self.scryfall_set_uri = None
        self.rulings_uri = None
        self.prints_search_uri = None
        self.collector_number = None
        self.digital = False
        self.rarity = None
        self.watermark = None
        self.card_back_id = None
        self.artist = None
        self.artist_ids = []
        self.illustration_id = None
        self.border_color = None
        self.frame = None
        self.frame_effects = []
        self.security_stamp = None
        self.full_art = False
        self.textless = False
        self.booster = False
        self.story_spotlight = False
        self.edhrec_rank = None
        self.preview = {}
        self.prices = {}
        self.related_uris = {}
        self.purchase_uris = {}
        self.card_faces = {}

        # self.fetch_card_data()

    def fetch_card_data(self):
        url = f'https://api.scryfall.com/cards/named?fuzzy={self.name}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            self.object = data.get("object")
            self.id = data.get("id")
            self.oracle_id = data.get("oracle_id")
            self.multiverse_ids = data.get("multiverse_ids", [])
            self.mtgo_id = data.get("mtgo_id")
            self.tcgplayer_id = data.get("tcgplayer_id")
            self.cardmarket_id = data.get("cardmarket_id")
            self.lang = data.get("lang")
            self.released_at = data.get("released_at")
            self.uri = data.get("uri")
            self.scryfall_uri = data.get("scryfall_uri")
            self.layout = data.get("layout")
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
            self.nonfoil = data.get("nonfoil", False)
            self.finishes = data.get("finishes", [])
            self.oversized = data.get("oversized", False)
            self.promo = data.get("promo", False)
            self.reprint = data.get("reprint", False)
            self.variation = data.get("variation", False)
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
            self.digital = data.get("digital", False)
            self.rarity = data.get("rarity")
            self.watermark = data.get("watermark")
            self.card_back_id = data.get("card_back_id")
            self.artist = data.get("artist")
            self.artist_ids = data.get("artist_ids", [])
            self.illustration_id = data.get("illustration_id")
            self.border_color = data.get("border_color")
            self.frame = data.get("frame")
            self.frame_effects = data.get("frame_effects", [])
            self.security_stamp = data.get("security_stamp")
            self.full_art = data.get("full_art", False)
            self.textless = data.get("textless", False)
            self.booster = data.get("booster", False)
            self.story_spotlight = data.get("story_spotlight", False)
            self.edhrec_rank = data.get("edhrec_rank")
            self.preview = data.get("preview", {})
            self.prices = data.get("prices", {})
            self.related_uris = data.get("related_uris", {})
            self.purchase_uris = data.get("purchase_uris", {})
            self.card_faces = data.get("card_faces")
        else:
            raise Exception("Failed to fetch data from Scryfall API")

    def to_dict(self):
        return {
            'quantity': self.quantity,
            'deck_category': self.deck_category,
            'name': self.name,
            'mana_cost': self.mana_cost,
            'cmc': self.cmc,
            'card_type': self.type_line,
            'card_description': self.oracle_text if self.card_faces == None else self.card_faces,
        }

    def set_quantity(self, quantity: str):
        if quantity != '':
            self.quantity = int(quantity)
        return 1


# Exemplo de uso:
# card = ScryfallCard("zaffai")
# print(card.name, card.oracle_text)

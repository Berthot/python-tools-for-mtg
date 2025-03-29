import json
from dataclasses import asdict
from typing import Optional, List
from uuid import UUID

from Clients.ScryfallClient import ScryfallClient
from Entities.Card import Card
from Entities.Deck import Deck
from Entities.Scryfall import Scryfall
from Repositories.ScryfallRepository import ScryfallRepository


class DeckService:
    def __init__(self):
        self.repository = ScryfallRepository()
        self.client = ScryfallClient()

    def update_deck_category_from_deck(self, deck: Deck, other_deck: Deck):
        """
        Atualiza as deck_category das cartas do deck com base nas deck_category do other_deck.
        """
        deck_category_map = {
            self.normalize(card.name): card.deck_category
            for card in other_deck.cards
            if card.deck_category
        }

        for card in deck.cards:
            key = self.normalize(card.name)
            if key in deck_category_map:
                card.deck_category = deck_category_map[key]

    def update_color_tag_from_deck(self, deck: Deck, other_deck: Deck):
        """
        Atualiza as tags de cor das cartas do deck com base nas tags de cor do other_deck.
        """
        deck_color_tag = {
            self.normalize(card.name): card.color_tag
            for card in other_deck.cards
            if card.color_tag
        }

        for card in deck.cards:
            key = self.normalize(card.name)
            if key in deck_color_tag:
                card.color_tag = deck_color_tag[key]

    def fetch_scryfall_data(self, deck_: Deck):
        """Busca os dados das cartas do deck no Scryfall e atualiza as cartas com os dados obtidos."""
        cards_to_fetch = []

        for card_ in deck_.cards:
            existing_card = self.repository.get_card_by_name(card_.name.strip().lower())
            if existing_card:
                card_.scryfall = existing_card
                card_.has_scryfall = True
            else:
                card_.has_scryfall = True
                cards_to_fetch.append(card_.get_primary_name())

        if cards_to_fetch:
            fetched_cards = self.client.get_cards_by_names(cards_to_fetch)
            # names = [fetched_card.get_primary_name() for fetched_card in fetched_cards]
            for card_in_deck in deck_.cards:
                name = card_in_deck.get_primary_name()
                scryfall_card = self.get_by_name(fetched_cards, name)
                if scryfall_card is None:
                    continue
                scryfall_name = scryfall_card.get_primary_name()
                if name == scryfall_name:
                    self.repository.add_card(scryfall_card)
                    card_in_deck.scryfall = scryfall_card
                    card_in_deck.has_scryfall = True
                if not card_in_deck.has_scryfall:
                    print(card_in_deck.name + ' :: not founded')

        self.repository.save_changes()

    @classmethod
    def get_by_name(cls, objects: List[Scryfall], name: str) -> Optional[Scryfall]:
        matches = list(filter(lambda obj: obj.get_primary_name() == name.lower(), objects))
        return matches[0] if matches else None

    @staticmethod
    def _card_to_dict(card: Card) -> dict:
        def default_serializer(obj):
            if isinstance(obj, UUID):
                return str(obj)
            raise TypeError(f"Type {type(obj)} not serializable")

        card_dict = asdict(card)
        if card.scryfall:
            card_dict['scryfall'] = asdict(card.scryfall)

        return json.loads(json.dumps(card_dict, default=default_serializer))

    @staticmethod
    def normalize(name: str) -> str:
        return name.split("//")[0].strip().lower()

# # Criando uma instância do DeckService
# deck_service = DeckService()
#
# # Criando um deck e adicionando algumas cartas
# deck = Deck()
# deck.add_card(Card.from_name("Lightning Bolt"))
# deck.add_card(Card.from_name("Counterspell"))
# deck.add_card(Card.from_name("Shock"))
#
# # Buscando os dados das cartas no Scryfall
# deck_service.fetch_scryfall_data(deck)
#
# # Exibindo as cartas do deck com os dados do Scryfall
# for card in deck.cards:
#     if card.has_scryfall:
#         print(f"Carta: {card.name}")
#         print(f"  Custo de Mana: {card.scryfall.mana_cost}")
#         print(f"  Tipo: {card.scryfall.type_line}")
#         print(f"  Texto Oracle: {card.scryfall.oracle_text}")
#         print("-" * 40)
#     else:
#         print(f"Carta não encontrada: {card.name}")

from Entities.Deck import Deck
from Entities.enums.EExportFormat import EExportFormat
from Services.DeckService import DeckService

LIGA = 'liga'
VILA = 'vila'
MANA_FIX = 'mana_fix'
PRIME_MTG = 'prime_mtg'
SUMMON = 'summon'
TAVERNA = 'taverna'
MERURU = 'meruru'
BLOOD = 'blood'
OTHER = 'other'

if __name__ == "__main__":
    deck_service = DeckService()
    main_deck_path = 'Files/main_deck.txt'  # Substitua pelo caminho correto do seu arquivo
    main_deck = Deck(main_deck_path)

    deck_service.fetch_scryfall_data(main_deck)

    main_deck.print_deck_list()

    main_deck.export(format=EExportFormat.JSON, full=False)
    main_deck.export(format=EExportFormat.ARCHIDEKT, full=False)


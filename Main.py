from Entities.Deck import Deck
from Entities.enums.EExportFormat import EExportFormat
from Services.DeckService import DeckService
from Services.LigaService import LigaService

# 🏪 Alias para nome de lojas
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
    liga_service = LigaService()

    # 📥 Carrega o primeiro deck a partir do arquivo
    first_deck_path = 'Files/first_deck.txt'
    first_deck = Deck(first_deck_path)

    # 📥 Carrega o segundo deck com categorias que queremos sincronizar
    second_deck_path = 'Files/second_deck.txt'
    second_deck = Deck(second_deck_path)

    # 🔄 Atualiza categorias do deck 1 com base no deck 2
    deck_service.update_deck_category_from_deck(deck=first_deck, other_deck=second_deck)

    # 🔄 Atualiza color_tags do deck 1 com base no deck 2
    deck_service.update_color_tag_from_deck(deck=first_deck, other_deck=second_deck)

    # 🔎 Busca informações das cartas via API do Scryfall
    deck_service.fetch_scryfall_data(first_deck)

    # 🖨️ Imprime o deck no terminal
    first_deck.print()

    # 💾 Exporta o deck como JSON simplificado
    # Arquivo exportado no path: Files/deck_list.json
    first_deck.export(format=EExportFormat.JSON, full=False)

    # 💾 Exporta o deck no formato Archidekt
    # Arquivo exportado no path: Files/archidekt.txt
    first_deck.export(format=EExportFormat.ARCHIDEKT, full=False)

    # 🌐 (Opcional) Abre abas do navegador com as cartas numa loja
    liga_service.buy_cards(deck=first_deck, store=VILA)

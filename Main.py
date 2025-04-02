from Entities.Deck import Deck
from Entities.enums.EExportFormat import EExportFormat
from Entities.enums.EStores import EStore
from Services.DeckService import DeckService
from Services.LigaService import LigaService


if __name__ == "__main__":
    deck_service = DeckService()
    liga_service = LigaService()
    # 📥 Carrega o primeiro deck a partir do arquivo
    first_deck = Deck(file_name='archidekt', use_generic_name=False)

    # 📥 Carrega o segundo deck com categorias que queremos sincronizar
    # second_deck = Deck(base_path='Files/other_deck_list.txt')

    # 🔄 Atualiza categorias do deck 1 com base no deck 2
    # deck_service.update_deck_category_from_deck(deck=first_deck, other_deck=second_deck)

    # 🔄 Atualiza color_tags do deck 1 com base no deck 2
    # deck_service.update_color_tag_from_deck(deck=first_deck, other_deck=second_deck)

    # 🔎 Busca informações das cartas via API do Scryfall
    deck_service.fetch_scryfall_data(first_deck)

    # 🖨️ Imprime o deck no terminal
    # first_deck.print(show=False)

    # 💾 Exporta o deck como JSON simplificado

    # first_deck.export(export_format=EExportFormat.JSON, full=False, internal_export=False)
    # first_deck.export(export_format=EExportFormat.ARCHIDEKT, full=False, internal_export=False)

    # first_deck.export(export_format=EExportFormat.LIGA, full=False, internal_export=False)

    # 💾 Exporta o deck no formato Archidekt
    # first_deck.export(export_format=EExportFormat.ARCHIDEKT, full=False, internal_export=True)

    # 🌐 (Opcional) Abre abas do navegador com as cartas numa loja
    # liga_service.buy_cards(deck=first_deck, store=EStore.LIGA, open_browser=True)

    buy_list_deck = Deck(file_name='buy_list', use_generic_name=True)
    buy_list_deck.print()

    deck_service.fetch_scryfall_data(buy_list_deck)
    buy_list_deck.export(export_format=EExportFormat.JSON, full=False, internal_export=True)

    # liga_service.buy_cards(deck=buy_list_deck, store=EStore.PLAYGROUND, open_browser=True)

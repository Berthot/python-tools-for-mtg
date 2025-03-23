from CardsManipulators.models.Deck import Deck

if __name__ == "__main__":
    file_path1 = 'datas/small_payload.txt'  # Substitua pelo caminho correto do seu arquivo
    deck1 = Deck(file_path1)

    file_path2 = 'datas/name_color_tag.txt'  # Substitua pelo caminho correto do seu arquivo
    deck2 = Deck(file_path2)

    # merge = deck1.update_color_tag_from_deck(deck2)


    deck1.fetch_all_scryfall_data()


    deck1.print_deck_list()

import json

from scryfall.models.ScryfallCard import ScryfallCard

def get_quantity(line: str):
    try:
        quantity = int(line.split()[0])
        if quantity > 0:
            return str(quantity)
    except (IndexError, ValueError):
        pass
    return ''

def has_quantity_in_line(quantity: str):
    try:
        if quantity == '':
            return False
    except (IndexError, ValueError):
        pass
    return True


def save_cards_to_json(input_file: str, output_file: str):
    cards = []
    acc = 0
    with open(input_file, 'r') as deck_file:
        file = deck_file.read().splitlines()

        for card_name in file:
            quantity = get_quantity(card_name)
            has_quantity = has_quantity_in_line(quantity)
            card_name =  " ".join(card_name.split(' ')[1:]) if has_quantity else card_name
            acc+=1
            print(f'[{acc}] -', end='')
            try:
                card = ScryfallCard(card_name)
                card.set_quantity(quantity)
                card_data = card.to_dict()
                print(card_data)  # Exibe os dados no console (opcional)
                cards.append(card_data)
            except:
                print(card_name + ' error searching')
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(cards, json_file, ensure_ascii=False, indent=4)

save_cards_to_json('cards.txt', 'cards.json')


# print(card.name)
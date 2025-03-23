def get_quantity(line: str):
    try:
        quantity = int(line.split('x ')[0])
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

def separe_cards(input_file: str, output_file: str):
    cards = []
    acc = 0
    getting = ' ^Getting,#2ccce4^'

    reuse_list = {}
    with open(r'/Helper/OLD_DECK.txt', 'r') as deck_reuse_file:
        file_reused = deck_reuse_file.read().split('\n')

        for reused_line in file_reused:
            reused_name = reused_line.split('(')[0].strip().split('x ')[1].strip()
            reused_tag = ' ^' + reused_line.split('^')[1].strip() + '^'
            reuse_list[reused_name] = reused_tag
            x = 1


    with open(f'D:/DEV/PYTHON/Magic-Python/Helper/{input_file}', 'r') as deck_file:
        file = deck_file.read().splitlines()

        for card_name in file:
            from_txt = card_name
            collection = '(' + from_txt.split('(')[1].strip().split('[')[0].strip()
            if '[' in card_name:
                card_my_category: str = card_name.split('[')[1].replace(']', '').strip().split('^')[0].strip()
            else:
                card_my_category: str = ''
            card_name = card_name.split('(')[0].strip().split('x ')[1].strip()
            quantity = get_quantity(from_txt)
            try:
                card_my_category = 'OUT_BY_GPT'
                card_data = quantity.replace('-','') + ' ' + card_name + ' ' + collection + ' [' + card_my_category + ']'
                if card_name not in reuse_list.keys():
                    acc += 1
                    # card_data += reuse_list[card_name]
                    card_data += " ^Don't Have,#f47373^"
                    cards.append(card_data)
                    print(f'[{acc}] -', end='')
                    print(card_data)  # Exibe os dados no console (opcional)

                else:
                    card_data += getting

            except:
                print(card_name + ' error searching')

    with open(f'D:/DEV/PYTHON/Magic-Python/Helper/{output_file}', 'w', encoding='utf-8') as json_file:
        json_file.writelines('\n'.join(cards))


separe_cards('NEW_DECK_WITH_CATEGORIES.txt', 'OQUE_SOBROU.txt')

# print(card.name)

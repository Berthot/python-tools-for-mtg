# import json
#
# from scryfall.models.ScryfallCard import ScryfallCard
#
# def get_quantity(line: str):
#     try:
#         quantity = int(line.split()[0])
#         if quantity > 0:
#             return str(quantity)
#     except (IndexError, ValueError):
#         pass
#     return ''
#
# def has_quantity_in_line(quantity: str):
#     try:
#         if quantity == '':
#             return False
#     except (IndexError, ValueError):
#         pass
#     return True
#
#
# def save_cards_to_json(input_file: str, output_file: str):
#     cards = []
#     acc = 0
#     with open(input_file, 'r') as deck_file:
#         file = deck_file.read().splitlines()
#
#         for card_name in file:
#             try:
#                 card = ScryfallCard(card_name)
#                 card_with_set = f'{card.name} [{card.set.upper()}]'
#                 print(card_with_set)
#                 cards.append(card_with_set)
#             except:
#                 print(card_name + ' error searching')
#     with open(output_file, 'w', encoding='utf-8') as json_file:
#         for i in cards:
#             json_file.write(f'{i}\n')
#
# save_cards_to_json('cards.txt', 'cards_tag.txt')
#
#
# # print(card.name)
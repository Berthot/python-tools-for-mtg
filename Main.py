from magic.Deck import Deck

VILA = 'vila'
MANA_FIX = 'mana_fix'
PRIME_MTG = 'prime_mtg'
SUMMON = 'summon'
TAVERNA = 'taverna'
MERURU = 'meruru'


deck = Deck(prefix='', suffix='', test=False)

deck.read_file(file_path='text_cards.txt', card_ready=True)

print(deck)

deck.buy_cards(store=VILA)

deck.write_in_file()


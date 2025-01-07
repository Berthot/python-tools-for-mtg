from magic.Deck import Deck

LIGA = 'liga'
VILA = 'vila'
MANA_FIX = 'mana_fix'
PRIME_MTG = 'prime_mtg'
SUMMON = 'summon'
TAVERNA = 'taverna'
MERURU = 'meruru'
BLOOD = 'blood'
OTHER = 'other'

deck = Deck(prefix='', suffix='', test=False)

deck.read_file(file_path='text_cards.txt', card_ready=True)

print(deck)

deck.buy_cards(store=LIGA)

deck.write_in_file()

# 3 Plains
# 3 Forest
# 3 Island
# 3 Mountain
# 3 Swamp

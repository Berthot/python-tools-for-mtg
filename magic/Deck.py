from magic.Card import Card, Font
import webbrowser


class Deck:
    def __init__(self, prefix: str = '', suffix: str = '', test: bool = False):
        self._test = test
        self.cards: [Card] = []
        self._total_lines = 0
        self.deck_size = len(self.cards)
        self._prefix = prefix
        self._suffix = suffix

    def add_card(self, card: Card):
        if card.is_valid:
            self.cards.append(card)

    def read_file(self, file_path: str, font: str = '', card_ready: bool = False):
        with open(f'files/{file_path}', 'r') as deck_file:
            file = deck_file.read().split('\n')
            self._total_lines = len(file)
            for i in file:
                card = Card(i, font, card_ready)
                if card.card_name in [x.card_name for x in self.cards]:
                    continue
                self.add_card(card)
                if self._test:
                    break
            self.deck_size = len(self.cards)

    def __str__(self):
        text = self.text_cards()
        # text += f'\nFrom Total: {self._total_lines}'
        text += f'\nDeck Size : {self.deck_size}'
        return text

    def text_cards(self):
        text = ''
        for i in self.cards:
            text += f'{self._append_prefix_suffix(i)}\n'
        return text

    def _append_prefix_suffix(self, i):
        if self._prefix != '':
            i = f'{self._prefix.strip()} {i}'
        if self._suffix != '':
            i = f'{i} {self._suffix}'
        return i

    def buy_cards(self, store: str = 'vila', limit: int = -1):
        var = input(f'digite sim para procurar na {store}')
        if var != 's':
            return
        acc = 0
        for card in self.cards:
            acc += 1
            webbrowser.open(Font.get_url(card.card_name, store))
            if acc == limit:
                break

    def write_in_file(self, file_name: str = 'file') -> None:
        with open(f'{file_name}.txt', 'w') as file:
            file.write(self.text_cards())

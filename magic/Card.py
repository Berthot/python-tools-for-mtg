class Font:
    to_buy_vila = 'to_buy_vila'
    bought_vila = 'bought_vila'
    liga = 'liga'

    @staticmethod
    def get_url(card_name: str, store: str) -> str:
        if store == 'vila':
            return f'https://www.vilacelta.com.br/?view=ecom%2Fitens&busca={card_name}'
        if store == 'taverna':
            return f'https://www.tavernagamehouse.com.br/?view=ecom%2Fitens&id=142722&searchExactMatch=&busca={card_name}&btnEnviar=1'
        if store == 'mana_fix':
            return f'https://www.manafix.net/?view=ecom%2Fitens&id=62691&searchExactMatch=&busca={card_name}&btnEnviar=1'
        if store == 'prime_mtg':
            return f'https://www.primemtg.com.br/?view=ecom%2Fitens&id=31113&searchExactMatch=&busca={card_name}'
        if store == 'summon':
            return f'https://www.summoner.com.br/?view=ecom%2Fitens&id=212593&searchExactMatch=&busca={card_name}&btnEnviar=1'
        if store == 'meruru':
            return f'https://www.meruru.com.br/?view=ecom%2Fitens&id=64102&searchExactMatch=&busca={card_name}&x=0&y=0'


class Card:
    def __init__(self, _input: str, _from: str, card_ready: bool = False):
        self._card_ready = card_ready
        self.is_valid = False
        self._from: str = _from
        self._ignore = self._ignore_list()
        self.card_name: str = self._set_card_name(possible_name=_input)

    def _set_card_name(self, possible_name: str) -> str:
        possible_name = possible_name.lower().replace('1x', '').strip()
        self._card_is_valid(possible_name)
        if not self.is_valid:
            return ''
        name = possible_name.split('/')[0].strip()
        if '(' in name:
            name = possible_name.split('/')[-1].strip().split('(')[0].strip()
        return name

    def _card_is_valid(self, _input: str):
        if _input == '':
            self.is_valid = False
            return
        for ignore in self._ignore_list():
            if ignore == _input or ignore in _input:
                self.is_valid = False
                return
        if ('/' not in _input) and not self._card_ready:
            self.is_valid = False
            return
        self.is_valid = True

    def __str__(self):
        return self.card_name

    @staticmethod
    def _ignore_list() -> [str]:
        return [
            'pten', 'português'
        ]

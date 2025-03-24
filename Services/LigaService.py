import webbrowser

from Entities.Deck import Deck


class LigaService:

    def buy_cards(self, deck: Deck, store: str = 'vila', limit: int = -1):
        acc = 0
        for card in deck.cards:
            acc += 1
            webbrowser.open(self.get_url(card.name, store))
            if acc == limit:
                break


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
        if store == 'liga':
            return f'https://www.ligamagic.com.br/?view=cards%2Fsearch&card={card_name}'
        if store == 'blood':
            return f'https://www.lojabloodmoon.com.br/?view=ecom%2Fitens&id=64102&searchExactMatch=&busca={card_name}'
        if store == 'other':
            return f'https://www.mineralgames.com.br/?view=ecom%2Fitens&id=9781&searchExactMatch=&busca={card_name}&btnEnviar=1'
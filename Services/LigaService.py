import webbrowser
from Entities.Deck import Deck
from Entities.enums.EStores import EStore


class LigaService:
    def buy_cards(self, deck: Deck, store: EStore = EStore.VILA, limit: int = -1, open_browser: bool = False) -> None:
        """
        Abre URLs para comprar as cartas do deck na loja especificada

        Args:
            deck: Deck contendo as cartas
            store: Loja para pesquisa (usar EStore.<opção>)
            limit: Número máximo de cartas para abrir (-1 = todas)
            open_browser: Defini se deve abrir ou não o browser
        """
        if not open_browser:
            return
        for i, card in enumerate(deck.cards, 1):
            webbrowser.open(self._get_store_url(card.name, store))
            if i == limit:
                break

    @staticmethod
    def _get_store_url(card_name: str, store: EStore) -> str:
        """
        Retorna a URL de busca para uma carta na loja especificada

        Args:
            card_name: Nome da carta
            store: Loja (do enum EStore)

        Returns:
            URL formatada para busca
        """
        # Mapeamento de lojas para URLs
        store_urls = {
            EStore.VILA: 'https://www.vilacelta.com.br/?view=ecom/itens&busca={card}',
            EStore.TAVERNA: 'https://www.tavernagamehouse.com.br/?view=ecom/itens&id=142722&busca={card}',
            EStore.MANA_FIX: 'https://www.manafix.net/?view=ecom/itens&id=62691&busca={card}',
            EStore.PRIME_MTG: 'https://www.primemtg.com.br/?view=ecom/itens&id=31113&busca={card}',
            EStore.SUMMON: 'https://www.summoner.com.br/?view=ecom/itens&id=212593&busca={card}',
            EStore.MERURU: 'https://www.meruru.com.br/?view=ecom/itens&id=64102&busca={card}',
            EStore.LIGA: 'https://www.ligamagic.com.br/?view=cards/search&card={card}',
            EStore.BLOOD: 'https://www.lojabloodmoon.com.br/?view=ecom/itens&id=64102&busca={card}',
            EStore.OTHER: 'https://www.mineralgames.com.br/?view=ecom/itens&id=9781&busca={card}'
        }

        return store_urls[store].format(card=card_name)

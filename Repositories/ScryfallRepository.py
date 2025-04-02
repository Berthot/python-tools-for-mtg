import os
from dataclasses import asdict, is_dataclass
from typing import List, Optional, Dict, Callable

import msgpack

from Entities.Scryfall import Scryfall


class ScryfallRepository:
    def __init__(self, file_path: str = "./Repositories/cards.msgpack"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(file_path, "wb") as file:
                file.write(msgpack.packb([], use_bin_type=True))
        self.cards: List[Scryfall] = self._load_cards()
        self.temporary: List[Scryfall] = []

    def _load_cards(self) -> List[Scryfall]:
        """Carrega as cartas do arquivo MessagePack."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "rb") as file:
                    file_content = file.read()
                    if not file_content:
                        return []
                    card_dicts = msgpack.unpackb(file_content, raw=False)
                    return [self._dict_to_card(card_dict) for card_dict in card_dicts]
            except Exception as e:
                print(f"Erro ao carregar o arquivo: {e}")
                return []
        return []

    def save_changes(self):
        """Salva as últimas alterações feitas (self.temporary) na lista e no arquivo com os dados."""
        self.cards.extend(self.temporary)
        card_dicts = [self._card_to_dict(card_item) for card_item in self.cards]
        with open(self.file_path, "wb") as file:
            file.write(msgpack.packb(card_dicts, use_bin_type=True))
        self.temporary.clear()

    def add_card(self, new_card: Scryfall):
        """
        Pega a carta recebida como parâmetro e adiciona à lista (self.temporary) de alterações.
        Verifica se a carta já existe para evitar duplicação.
        """
        if not self._card_exists(new_card):
            self.temporary.append(new_card)

    def add_range_card(self, new_cards: List[Scryfall]):
        """
        Pega as cartas recebidas como parâmetro e adiciona à lista (self.temporary) de alterações.
        Verifica se cada carta já existe para evitar duplicação.
        """
        for new_card in new_cards:
            if not self._card_exists(new_card):
                self.temporary.append(new_card)

    def _card_exists(self, card_to_check: Scryfall) -> bool:
        """
        Verifica se a carta já existe na lista temporária ou na lista principal.
        """
        if any(existing_card.name == card_to_check.name for existing_card in self.temporary):
            return True
        if any(existing_card.name == card_to_check.name for existing_card in self.cards):
            return True
        return False

    def get_card_by_name(self, card_name: str) -> Optional[Scryfall]:
        """Retorna uma carta pelo nome (self.cards)."""
        return next((card for card in self.cards if card.get_primary_name() == card_name), None)

    def get_cards(self) -> List[Scryfall]:
        """Retorna cartas como se fosse feito um 'where' na lista de cartas (self.cards)."""
        return self.cards

    def where(self, filter_func: Callable[[Scryfall], bool]) -> List[Scryfall]:
        """
        Filtra as cartas no repositório com base numa função de filtro.

        Args:
            filter_func: Uma função que recebe um objeto Scryfall e retorna True ou False.

        Returns:
            Uma lista de objetos Scryfall que atendem ao critério do filtro.
        """
        return [card for card in self.cards if filter_func(card)]

    @staticmethod
    def _card_to_dict(card_to_convert: Scryfall) -> Dict:
        """
        Converte um objeto Card num dicionário.
        Converte o campo 'id' (UUID) numa 'string' para serialização.
        """
        if is_dataclass(card_to_convert) and isinstance(card_to_convert, Scryfall):
            card_dict = asdict(card_to_convert)
            card_dict["id"] = str(card_dict["id"])
            return card_dict
        raise ValueError("O objeto não é uma instância de Card.")

    @staticmethod
    def _dict_to_card(card_dict: Dict) -> Scryfall:
        """
        Converte um dicionário de volta para um objeto Card.
        Converte o campo 'id' (‘string’) de volta para UUID.
        """
        card_object = Scryfall()
        card_object.advanced_scryfall_data(card_dict)
        return card_object

# # Criando uma instância do CardRepository
# repository = ScryfallRepository()
# print(len(repository.cards))
#
# # Criando algumas cartas
# card1 = Scryfall(name="Lightning Bolt")
# card2 = Scryfall(name="Counterspell")
#
# # Adicionando cartas ao repositório
# repository.add_card(card1)
# repository.add_card(card2)
# # repository.add_card(card3)
#
# # Salvando as alterações
# repository.save_changes()
#
# # Buscando uma carta pelo nome
# found_card = repository.get_card_by_name("Lightning Bolt")
# shock_card = repository.get_card_by_name("sol ring")
# print(shock_card)
# if found_card:
#     print(found_card)  # Exibe o objeto Card
#
# # Buscando todas as cartas
# all_cards = repository.get_cards()
# for card in all_cards:
#     print(card)


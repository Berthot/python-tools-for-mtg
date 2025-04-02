from enum import Enum


class EStore(Enum):
    """
    Enumeração de lojas de Magic: The Gathering.
    Digite 'EStore.' para ver todas as opções disponíveis.

    Opções:
        LIGA: 'liga'
        VILA: 'vila'
        MANA_FIX: 'mana_fix'
        PRIME_MTG: 'prime_mtg'
        SUMMON: 'summon'
        TAVERNA: 'taverna'
        MERURU: 'meruru'
        BLOOD: 'blood'
        OTHER: 'other'
    """
    PLAYGROUND = 'playground'
    LIGA = 'liga'
    VILA = 'vila'
    MANA_FIX = 'mana_fix'
    PRIME_MTG = 'prime_mtg'
    SUMMON = 'summon'
    TAVERNA = 'taverna'
    MERURU = 'meruru'
    BLOOD = 'blood'
    OTHER = 'other'

    @classmethod
    def from_alias(cls, alias: str) -> 'EStore':
        """Converte um alias (string) para o enum correspondente (case-insensitive)"""
        alias = alias.lower().strip()
        for store in cls:
            if store.value == alias:
                return store
        raise ValueError(f"Alias inválido: {alias}. Opções válidas: {[e.value for e in cls]}")

    def __str__(self) -> str:
        return self.value
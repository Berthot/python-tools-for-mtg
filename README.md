# 🐍 Python Tools for 🧙‍♂️ Magic Players

> Um conjunto de ferramentas escritas em Python para jogadores de Magic: The Gathering 🎴, com foco em leitura de decks exportados do [Archidekt](https://www.archidekt.com/) 📥 e integração com a API do [Scryfall](https://scryfall.com/) 🔍.

## Visão Geral ✨

Este projeto tem como objetivo facilitar a manipulação e análise de decks de Magic: The Gathering de forma simples, rápida e extensível. Com ele, você pode:

- 📄 Carregar decks exportados do Archidekt (em formato texto)
- 🔍 Buscar informações detalhadas das cartas usando a API do Scryfall
- 💾 Salvar localmente os dados para reuso com MessagePack
- 🛒 Abrir links para comprar cartas nas principais lojas brasileiras com 1 linha de código

Ideal para jogadores de Commander, colecionadores e desenvolvedores que curtem MTG e Python!

## Funcionalidades

- ✅ Leitura de arquivos `.txt` exportados do Archidekt
- ✅ Enriquecimento de dados via Scryfall (nome, tipo, oracle text, etc.)
- ✅ Busca local e persistência de cartas para evitar chamadas repetidas
- ✅ Geração de arquivos JSON a partir de decks
- ✅ Abertura de links de compra diretamente no navegador — basta informar a URL da loja ou usar um nome pré-definido.


## Como usar

### 1. Instalação

Recomenda-se usar um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt  # se aplicável
```

### 2. Estrutura dos arquivos

- `Deck.py`: classe principal para carregar e manipular decks
- `Card.py`: representa uma carta individual
- `ScryfallClient.py`: cliente para consumir a API do Scryfall
- `ScryfallRepository.py`: repositório local de cartas salvas
- `DeckService.py`: orquestra o carregamento de dados e interações
- `LigaService.py`: gera URLs para lojas

### 3. Exemplo de uso básico

```python
from Services.DeckService import DeckService
from Entities.Deck import Deck

# Carrega deck exportado do Archidekt
deck = Deck("./meu_deck.txt")

# Instancia o serviço e busca os dados
service = DeckService()
service.fetch_scryfall_data(deck)

# Exibe as cartas com dados completos
deck.print_deck_list()

# Salva como JSON
service.save_deck_in_json(deck)

# Abrir links para compra (opcional)
service.buy_cards(deck, store='vila')
```

## Formato aceito (exportado do Archidekt)

```
1x Phyrexian Tower (mh3) 303 [Land] ^Have,#37d67a^
1x Yahenni, Undying Partisan (tdc) 202 [Sacrifice Outlets] ^Have,#37d67a^
1x Dictate of Erebos (plst) JOU-65 [Payoffs/Anthems] ^Have,#37d67a^
1x Black Market Connections (acr) 87 [Card Draw] ^Have,#37d67a^
1x Elenda, the Dusk Rose (lcc) 268 [Commander{top}] ^Have,#37d67a^
1x Athreos, God of Passage (plst) JOU-146 [Recursion] ^Don't Have,#f47373^
```

```json
{
    "quantity": 1,
    "name": "Phyrexian Tower",
    "deck_category": "Land",
    "mana_cost": "",
    "cmc": 0,
    "card_type": "Legendary Land",
    "card_description": "{T}: Add {C}.\n{T}, Sacrifice a creature: Add {B}{B}."
}
```

- Quantidade + Nome
- Coleção opcional
- Categoria entre colchetes `[Mainboard]`, `[Sideboard]`, etc
- Tag de cor opcional `^Red^`, `^Blue^`, etc

## Requisitos

- Python 3.9+
- Bibliotecas:
  - `requests`
  - `msgpack`

## Status

Projeto pessoal em andamento e com foco educativo. Feel free to fork, sugerir melhorias ou usar como base!

---

Feito com ❤️ por um jogador de Commander que também ama Python.
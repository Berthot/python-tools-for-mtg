with open('decks/myrkur_completo.txt', 'r') as deck1:
    completo = deck1.read().lower().split('\n')
    deck_a = len(completo)

with open('decks/myrkur_comprados.txt', 'r') as deck2:
    comprado = deck2.read().lower().split('\n')
    deck_b = len(comprado)

with open('falta_comprar_deck.txt', 'w') as file:
    for carta in completo:
        if carta.lower() not in comprado:
            print(carta)
            # continue
            file.write(f'{carta} \\ \n')


print(f"a: [{deck_a}]")
print(f"b: [{deck_b}]")
print(f"falta comprar: [{abs(deck_b - deck_a)}]")

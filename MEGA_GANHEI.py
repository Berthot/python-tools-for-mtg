import hashlib
import random

mix = ''

def get_winner_senna(name: str, birth: str):
    mix = name + ' nascido em ' + birth
    hash_result = hashlib.sha256(mix.encode()).hexdigest()
    random.seed(hash_result)
    values = set()
    while len(values) < 6:
        value = random.randint(1, 60)
        values.add(value)
    return sorted(values)

name_value = "Maria De Lourdes Dela Coleta Bertho"
birth_value = "02/04/1952"
key = name_value + ' nascido em ' + birth_value
numeros_megasena = get_winner_senna(name_value, birth_value)
print(f"KEY: [{key}]", numeros_megasena)



# KEY: [Maria De Lourdes Dela Coleta Bertho nascido em 02/04/1952] [9, 11, 12, 22, 37, 60]
# KEY: [Cristiane Cacilda Bertho nascido em 25/12/1972] [2, 22, 34, 46, 47, 55]
# KEY: [Matheus Bertho Tavares nascido em 03/04/1998]   [1, 4,  6,  25, 40, 49]
# KEY: [chute]                                          [03, 14, 19, 27, 39,50]



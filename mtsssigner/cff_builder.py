# d-CFF(t,n)
# t = número de testes
# n = número de blocos
# d = número de erros detectáveis
# resultado da construção da cff -> d-CFF(q², q^k)
# q -> potência de primos

# imagem (resultados possíveis) de q = ????

import galois
from galois import FieldArray

from utils import is_prime_power

def create_cff(q: int, k: int):
    assert is_prime_power(q)
    assert k >= 2

    finite_field: FieldArray = galois.GF(q)
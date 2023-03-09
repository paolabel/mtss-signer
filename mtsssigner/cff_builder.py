# d-CFF(t,n)
# t = número de testes
# n = número de blocos
# d = número de erros detectáveis
# resultado da construção da cff -> d-CFF(q², q^k)
# q -> potência de primos

# imagem (resultados possíveis) de q = ????

import galois
from galois import FieldArray
from math import inf

from utils import is_prime_power, get_cartesian_product, get_polynomials_with_deg_up_to_k

import numpy
from numpy.polynomial import Polynomial

def get_b_set(field: FieldArray, k: int) -> list[Polynomial]:
    order: int = field.order
    # assume que elementos do corpo finito sempre são "contínuos"
    field_elements: list = [x for x in range(order)]
    polinomial_ring_coeffs: list[list] = get_cartesian_product(field_elements)
    polinomial_coeffs_with_deg_up_to_k = get_polynomials_with_deg_up_to_k(polinomial_ring_coeffs, k)
    b_set = [Polynomial(coefficients) for coefficients in polinomial_coeffs_with_deg_up_to_k]
    return b_set

def create_cff(q: int, k: int):
    assert is_prime_power(q)
    assert k >= 2

    finite_field: FieldArray = galois.GF(q)
    print(finite_field.properties)
    
    
if __name__ == '__main__':
    sett = get_b_set(galois.GF(4), 3)
    for element in sett:
        print(str(element).replace('.0', '').replace('·', '').replace('x¹', 'x'))
    
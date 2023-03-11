# d-CFF(t,n)
# t = número de testes
# n = número de blocos
# d = número de erros detectáveis
# resultado da construção da cff -> d-CFF(q², q^k)
# q -> potência de primos

# imagem (resultados possíveis) de q = ????

from typing import List
import galois
from galois import FieldArray
from math import inf
import itertools
import numpy
import sys

from utils import is_prime_power, get_all_coefficient_combinations_in_field, get_polynomials_with_deg_up_to_k, get_field_elements, print_polynomial_list, get_polynomial_value_at_x

from numpy.polynomial import Polynomial

# TODO criar função de construção para 1-CFF 
# e função que escolhe qual construção usar dependendo se d = 1 ou não


def get_b_set(field: FieldArray, k: int) -> List[Polynomial]:
    polinomial_ring_coeffs: list[list] = get_all_coefficient_combinations_in_field(field)
    polinomial_coeffs_with_deg_up_to_k = get_polynomials_with_deg_up_to_k(polinomial_ring_coeffs, k)
    b_set = [Polynomial(coefficients) for coefficients in polinomial_coeffs_with_deg_up_to_k]
    return b_set

# transformar cada elemento em um Point?
def get_x_set(field: FieldArray) -> List[list]:
    field_elements: List[int] = get_field_elements(field)
    result = itertools.product(field_elements, repeat=2)
    return [tuple(element) for element in result]

def create_polynomial_cff(q: int, k: int):
    assert is_prime_power(q)
    assert k >= 2

    # talvez não precise checar se q é potência de primo pq o construtor da GF já o faz
    finite_field: FieldArray = galois.GF(q)
    b_set = get_b_set(finite_field, k)
    x_set = get_x_set(finite_field)
    
    cff_dimensions = (q**2, q**k)
    cff = numpy.zeros(cff_dimensions, dtype=int)
    
    for test in range(cff_dimensions[0]):
        for block in range(cff_dimensions[1]):
            if ((get_polynomial_value_at_x(b_set[block], x_set[test][0]) % q) == x_set[test][1]):
                cff[test][block] = 1

    return cff
     
if __name__ == '__main__':
    numpy.set_printoptions(threshold=sys.maxsize)
    print(create_polynomial_cff(3,2))
    
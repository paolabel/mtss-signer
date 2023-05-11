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
from math import inf, sqrt, log, comb
import itertools
import numpy
import sys
from utils.math_utils import get_all_coefficient_combinations_in_field, get_polynomials_with_deg_up_to_k, get_field_elements, get_polynomial_value_at_x
from utils.prime_utils import is_prime_power
from numpy.polynomial import Polynomial

def get_b_set(field: FieldArray, k: int) -> List[Polynomial]:
    polinomial_ring_coeffs: list[list] = get_all_coefficient_combinations_in_field(field)
    polinomial_coeffs_with_deg_up_to_k = get_polynomials_with_deg_up_to_k(polinomial_ring_coeffs, k)
    b_set = [Polynomial(coefficients) for coefficients in polinomial_coeffs_with_deg_up_to_k]
    return b_set

def get_x_set(field: FieldArray) -> List[list]:
    field_elements: List[int] = get_field_elements(field)
    result = itertools.product(field_elements, repeat=2)
    return [tuple(element) for element in result]

def create_cff(q: int, k:int) -> List[list]:
    d: int = get_d(q, k)
    if d == 1:
        return create_1_cff(q**k)
    else:
        return create_polynomial_cff(q, k)

def create_1_cff(n: int) -> List[list]:
    t: int = get_t_for_1_cff(n)
    tests: List[list] = get_1_cff_columns(t)
    cff = numpy.zeros((t,n), dtype=int)
    for block in range(n):
        for incidence in tests[block]:
            cff[incidence][block] = 1
    return cff

def get_t_for_1_cff(n: int):
    # binomial coefs. values for (t floor(t/2))
    # binomial_coefficient_results[2] = binomial coefficient (2 1)
    # espera-se que não será assinado documento com mais de 6435 blocos 
    binomial_coefficient_results = [1, 1, 2, 3, 6, 10, 20, 35, 70, 126, 252, 462, 924, 1716, 3432, 6435]
    if n > 6435:
        t = 15
        result = 6435
        while result < n:
            t+= 1
            result = comb(t, numpy.floor(t/2))
        return t
    else:
        for index in range(1, len(binomial_coefficient_results)):
            if binomial_coefficient_results[index] >= n:
                return index

def get_1_cff_columns(t: int):
    result = itertools.combinations(range(t), int(numpy.floor(t/2)))
    return list(result)

def create_polynomial_cff(q: int, k: int) -> List[list]:
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

def get_q(k:int, d: int):
    q:int = d(k-1) + 1
    return q

def get_q_from_error_and_block_number(d: int, b: int):
    pass

def get_d(q:int, k:int):
    if k < 2:
        return 0
    if not is_prime_power(q):
        return 0
    d: int = int(numpy.floor((q-1)/(k-1)))
    return d 

def get_d_from_test_and_block_number(t: int, b: int):
    q: int = int(sqrt(t))
    assert is_prime_power(q)
    k: int = get_k_from_b_and_q(b, q)
    return get_d(q, k)

def get_k_from_b_and_q(b: int, q: int):
    return int(log(b,q))

if __name__ == '__main__':
    numpy.set_printoptions(threshold=sys.maxsize)
    print(get_d(3,2))


from typing import List
from math import sqrt, log, comb
import itertools
import galois
from galois import FieldArray
import numpy
from numpy.polynomial import Polynomial
from sympy import factorint
from mtsssigner import logger
from mtsssigner.utils.math_utils import (get_all_polynomials_with_deg_up_to_k,
                                        get_field_elements,
                                        get_polynomial_value_at_x)
from mtsssigner.utils.prime_utils import is_prime_power

# Creates either a 1-CFF or a polynomial d-CFF, according to the obtainable
# amount of max modifiable blocks (d) provided by the parameters q and k.
def create_cff(q: int, k:int) -> List[List[int]]:
    d: int = get_d(q, k)
    if d == 1 or k < 2:
        return create_1_cff(q**k)
    return __create_polynomial_cff(q, k)

# Creates an 1-CFF with the minimum amount of
# tests possible (using Sperner set systems)
def create_1_cff(n: int) -> List[List[int]]:
    t: int = get_t_for_1_cff(n)
    tests: List[list] = __get_1_cff_columns(t)
    cff = numpy.zeros((t,n), dtype=int)
    for block in range(n):
        for incidence in tests[block]:
            cff[incidence][block] = 1
    return cff

# Returns the number of tests required for building
# an optimal 1-CFF(n) using Sperner set systems
def get_t_for_1_cff(n: int) -> int:
    # List containing binomial coefs. values for (t floor(t/2))
    # Example: binomial_coefficient_results[2] = binomial coefficient (2 1)
    binomial_coefficient_results = [1, 1, 2, 3, 6, 10, 20, 35, 70, 126,
                                    252, 462, 924, 1716, 3432, 6435]
    if n > 6435:
        t = 15
        result = 6435
        while result < n:
            t+= 1
            result = comb(t, numpy.floor(t/2))
        return t
    for index in range(1, len(binomial_coefficient_results)):
        if binomial_coefficient_results[index] >= n:
            return index

# Returns the columns of an optimal 1-CFF, built using every
# combination of floor(t/2) elements each from the column
def __get_1_cff_columns(t: int) -> List[int]:
    result = itertools.combinations(range(t), int(numpy.floor(t/2)))
    return list(result)

# Creates a d-CFF(q^2, q^k) using a polynomial construction.
# Considering its construction, q must be a prime power and k must
# be equal or bigger than 2, and k cannot not be bigger than q. If k = 2,
# the CFF can be built, but it results in less modifiable blocks in the
# final signed document, compared to hashing each block individually,
# considering the resulting signature size. If q = k, the polynomial
# 1-CFF is less eficient in size than an optimal 1-CFF.
def __create_polynomial_cff(q: int, k: int) -> List[List[int]]:
    assert is_prime_power(q)
    assert k >= 2
    assert q >= k

    finite_field: FieldArray = galois.GF(q)
    b_set = __get_b_set(finite_field, k)
    x_set = __get_x_set(finite_field)

    cff_dimensions = (q**2, q**k)
    cff = numpy.zeros(cff_dimensions, dtype=int)

    for test in range(cff_dimensions[0]):
        for block in range(cff_dimensions[1]):
            if (get_polynomial_value_at_x(b_set[block], x_set[test][0]) % q) == x_set[test][1]:
                cff[test][block] = 1

    return cff

# Returns the B set for constructing a polynomial CFF
def __get_b_set(field: FieldArray, k: int) -> List[Polynomial]:
    polinomial_coeffs_with_deg_up_to_k: list[list] = get_all_polynomials_with_deg_up_to_k(field, k)
    b_set = [Polynomial(coefficients) for coefficients in polinomial_coeffs_with_deg_up_to_k]
    return b_set

# Returns the X set for constructing a polynomial CFF
def __get_x_set(field: FieldArray) -> List[list]:
    field_elements: List[int] = get_field_elements(field)
    result = itertools.product(field_elements, repeat=2)
    return [tuple(element) for element in result]

# Gets the d value for the d-CFF according to the relation d = floor((q-1)/(k-1))
def get_d(q:int, k:int) -> int:
    if k < 2:
        return 0
    if not is_prime_power(q):
        return 0
    d: int = int(numpy.floor((q-1)/(k-1)))
    return d

# Gets the q value for the d-CFF(q^2,n=q^k) according to a supplied k
# and the desired number of blocks (n). Available k values supplied in
# case of incorrect k input are not correct for prime powers q^k whose
# k contains more than 2 factors (e.g. 2^30)
def get_q_from_k_and_n(k:int, n:int) -> int:
    q = round(numpy.power(n, (1/k)))
    if q**k != n:
        n_factors: dict = factorint(n)
        compatible_k = []
        for exponent in n_factors.values():
            exponent_factors = factorint(exponent)
            compatible_k.append(exponent)
            if len(exponent_factors) == 1:
                break
            for factor in exponent_factors:
                compatible_k.append(factor)
                if exponent_factors[factor] == 1:
                    continue
                compatible_k.append(factor*exponent_factors[factor])
                factors = exponent_factors.keys()
                multiplication = 1
                for factor in factors:
                    multiplication *= factor
                compatible_k.append(multiplication)
        compatible_k.sort()
        error_message = (
            f"Provided 'k' = {k} cannot provide answer compatible with block number = {n}.\n"
            f"Compatible 'k' values may be one the following: {compatible_k}."
        )
        logger.log_error(error_message)
        raise ValueError(error_message)
    return q

# Gets the k value for the d-CFF(t=q^2,n=q^k) according to
# the desired number of blocks (n) and a given q
def get_k_from_n_and_q(n: int, q: int) -> int:
    k = round(log(n,q))
    if q**k != n:
        n_factors: dict = factorint(n)
        error_message = (
            f"\n   Provided 'q' = {q} cannot provide answer compatible with block number = {n}.\n"
            f"   Compatible 'q' values may be one the following: {list(n_factors.keys())}.\n"
             "   If you are signing a messgage with a desired maximum signature size, the size "
             "supplied is rounding to an incompatible number of tests.\n"
             "   If you are verifying a signature, the number of blocks of the modified file is "
             "different from the original message."
        )
        logger.log_error(error_message)
        raise ValueError(error_message)
    return k

# Gets the q value for the d-CFF according to the relation d = floor((q-1)/(k-1))
# Not used
def __get_q(k:int, d: int) -> int:
    q:int = d(k-1) + 1
    return q

# Gets the d value for the d-CFF(t=q^2,n=q^k) according to the
# desired number of tests (t) and the desired number of blocks (n)
# Not used
def __get_d_from_test_and_block_number(t: int, n: int) -> int:
    q: int = int(sqrt(t))
    assert is_prime_power(q)
    k: int = get_k_from_n_and_q(n, q)
    return get_d(q, k)

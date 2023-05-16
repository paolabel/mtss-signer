from itertools import chain, combinations
import itertools
from typing import List
from numpy.polynomial import Polynomial
import numpy
from galois import FieldArray

# ainda não sei se preciso
# https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def get_powerset(iterable: set) -> list:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, length) for length in range(len(s)+1))

# https://stackoverflow.com/questions/533905/how-to-get-the-cartesian-product-of-multiple-lists
def get_all_polynomials_with_deg_up_to_k(field: FieldArray, k: int) -> List[list]:
    # assume que sempre vai retornar a mesma ordem
    field_elements = get_field_elements(field)
    result = itertools.product(field_elements, repeat=k)
    returnval = list()
    for element in result:
        coefs = list(element)
        coefs.reverse()
        returnval.append(coefs)
    return returnval

def get_polynomial_value_at_x(polynomial: Polynomial, x: int) -> int:
    coefficients = list(polynomial.coef)
    coefficients.reverse()
    value = int(numpy.polyval(coefficients, x))
    return value

def get_field_elements(field: FieldArray) -> List[int]:
    order: int = field.order
    # assume que elementos do corpo finito sempre tem elementos contínuos
    field_elements: list = [x for x in range(order)]
    return field_elements

def print_polynomial_list(polynomial_list: List[Polynomial]):
    for element in polynomial_list:
        print(str(element).replace('.0', '').replace('·', '').replace('x¹', 'x'))

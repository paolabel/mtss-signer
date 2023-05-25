import itertools
from typing import List
from numpy.polynomial import Polynomial
import numpy
from galois import FieldArray

# https://stackoverflow.com/questions/533905/how-to-get-the-cartesian-product-of-multiple-lists
# Returns the list of all polynomials of degree up to k, where
# its coefficients are all members of a given finite field
def get_all_polynomials_with_deg_up_to_k(field: FieldArray, k: int) -> List[list]:
    # assume que sempre vai retornar a mesma ordem
    field_elements = get_field_elements(field)
    result = itertools.product(field_elements, repeat=k)
    returnval = []
    for element in result:
        coefs = list(element)
        coefs.reverse()
        returnval.append(coefs)
    return returnval

# Evaluates a polynomial function at x
def get_polynomial_value_at_x(polynomial: Polynomial, x: int) -> int:
    coefficients = list(polynomial.coef)
    coefficients.reverse()
    value = int(numpy.polyval(coefficients, x))
    return value

# Gets the elements of a finite field
def get_field_elements(field: FieldArray) -> List[int]:
    order: int = field.order
    # Assumes that the elements of a finite field are always continuous
    field_elements: list = list(range(order))
    return field_elements

# Pretty prints a list of Polynomial objects
def print_polynomial_list(polynomial_list: List[Polynomial]):
    for element in polynomial_list:
        print(str(element).replace('.0', '').replace('·', '').replace('x¹', 'x'))

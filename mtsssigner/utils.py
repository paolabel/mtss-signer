import math
from itertools import chain, combinations
import itertools
from typing import List
from numpy.polynomial import Polynomial
import numpy
from galois import FieldArray

# https://geekflare.com/prime-number-in-python/
def is_prime(number: int) -> bool:
    for factor in range(2,int(math.sqrt(number))+1):
        if (number%factor) == 0:
            return False
    return True

# https://www.quora.com/How-can-we-check-if-a-number-is-prime-power
def is_prime_power(number:int) -> bool:
    power_range = int(math.log(number, 2)) 
    for power in range(1,power_range+1):
        if power == 1:
            root = number 
        elif power == 2:
            root = int(math.sqrt(number)) 
        else:
            # https://stackoverflow.com/questions/19255120/is-there-a-short-hand-for-nth-root-of-x-in-python
            root = int(round(math.exp(math.log(number)/power), 0)) 
            # ou root = int(round(x**(1/n)))
        if (number == (root**power) and is_prime(root)): 
            return True
    return False

# ainda não sei se preciso
# https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def get_powerset(iterable: set) -> list:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, length) for length in range(len(s)+1))

# https://stackoverflow.com/questions/533905/how-to-get-the-cartesian-product-of-multiple-lists
def get_all_coefficient_combinations_in_field(field: FieldArray) -> List[list]:
    # assume que sempre vai retornar a mesma ordem
    field_elements = get_field_elements(field)
    result = itertools.product(field_elements, repeat=len(field_elements))
    returnval = list()
    for element in result:
        coefs = list(element)
        coefs.reverse()
        returnval.append(coefs)
    return returnval

def get_polynomials_with_deg_up_to_k(polynomial_coefficients: List[list], k: int):
    updated_polynomial_coefficients = list(list())
    for polynomial_coefficient in polynomial_coefficients:
        updated_polynomial_coefficient = polynomial_coefficient[:k]
        if updated_polynomial_coefficient not in updated_polynomial_coefficients:
            updated_polynomial_coefficients.append(updated_polynomial_coefficient)
    return updated_polynomial_coefficients

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
    
if __name__ == '__main__':
    print(get_all_coefficient_combinations_in_field([0,1,2,3]))
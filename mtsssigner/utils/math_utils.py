import itertools
from typing import List
from numpy.polynomial import Polynomial
from galois import FieldArray, Poly

# https://stackoverflow.com/questions/533905/how-to-get-the-cartesian-product-of-multiple-lists
# Returns the list of all polynomials of degree up to k, where
# its coefficients are all members of a given finite field
def get_all_polynomials_with_deg_up_to_k(field: FieldArray, k: int) -> List[Poly]:
    result = itertools.product(field.elements, repeat=k)
    return [Poly(coefs, field=field) for coefs in result]

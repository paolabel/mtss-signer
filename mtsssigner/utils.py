import math
from itertools import chain, combinations
import itertools
from galois import FieldArray
from collections import OrderedDict

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
def get_cartesian_product(iterable: list) -> list:
    result = itertools.product(iterable, repeat=len(iterable))
    return [list(element) for element in result]

def get_polynomial_ring_from_field(field: FieldArray):
    pass



if __name__ == '__main__':
    print(get_cartesian_product([0,1,2,3,4]))
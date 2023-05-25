from typing import Dict
from math import log
import numpy
from mtsssigner.cff_builder import get_d, get_t_for_1_cff
from mtsssigner.utils.prime_utils import basic_prime_power_sequence, is_prime_power

# Return a grid where the lines are q values, columns are k values,
# and the cells contain the resulting d number for the parameters q and k,
# considering their relation follows the function d = floor((q-1)/(k-1)).
# The values start at q and k = 2, since smaller values of q always result in d = 0
# and k must start at 2 according to its definition in the creation of polynomial CFFs
def get_results_grid():
    grid = numpy.zeros((20,30), dtype=int)
    for q in range(2, len(grid)):
        if not is_prime_power(q):
            continue
        for k in range(2, len(grid[q])):
            grid[q][k] = get_d(q, k)
    for q in range(len(grid)):
        print(f"q={q} {grid[q]}")
    return grid

# Returns a dict containing the total amount and proportion
# of modifiable blocks for a given number of blocks
def get_max_d_proportion():
    proportions = {}
    k = 3
    for q in range(102):
        if not is_prime_power(q):
            continue
        d = get_d(q, k)
        if d > 1:
            n = q**k
            t = q**2
            proportion = d/n
            proportions[n] = f"{round(proportion*100, 4)}% ({d}-CFF({t},{n}) com q={q} e k={3})"
    return proportions

# Returns a dict which contain the polynomial CFFs that can be created with the number
# of blocks supplied, indexed by their max number of allowed modification of blocks (d)
def get_possible_CFFs_from_n(n: int) -> Dict:
    possible_d_and_t = {}
    for q in basic_prime_power_sequence:
        k = log(n, q)
        if k - int(k) == 0.0 and k > 1:
            k = int(k)
            d = get_d(q, k)
            if d == 1:
                possible_d_and_t[d] = f"1-CFF({get_t_for_1_cff(n)}, {n}), q={q}, k={k}"
                continue
            if d > 0:
                possible_d_and_t[d] = f"{d}-CFF({q**2}, {q**k}), q={q}, k={k}"
    return possible_d_and_t

import numpy
from mtsssigner.cff_builder import get_d, get_t_for_1_cff
from typing import Dict
from math import log
from prime_utils import basic_prime_power_sequence, is_prime_power

def get_results_grid():
    grid = numpy.zeros((20,30), dtype=int)
    for q in range(len(grid)):
        if not is_prime_power(q):
            continue
        for k in range(len(grid[q])):
            grid[q][k] = get_d(q, k)
    for q in range(len(grid)):
        print(f"q={q} {grid[q]}")
    return grid

# Returns a dict containing the max amount and proportion of modifiable blocks
# for a given number of blocks
def get_max_d_proportion():
    proportions = dict()
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

# Returns a dict where the keys are the allowed number of modifications
# and the values are the number of tests required to build the cff
# for the desired number of blocks
def get_possible_d_and_t_from_b(n: int) -> Dict:
    possible_d_and_t = dict()
    for q in basic_prime_power_sequence:
        k = log(n, q)
        if k - int(k) == 0.0 and k > 1:
            d = get_d(q, int(k))
            if d == 1:
                possible_d_and_t[d] = get_t_for_1_cff(n)
                continue
            if d > 0:
                possible_d_and_t[d] = q**2
    return possible_d_and_t

if __name__ == '__main__':
    print(get_possible_d_and_t_from_b(729))

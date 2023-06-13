from mtsssigner.cff_builder import *
from timeit import default_timer as timer
from datetime import timedelta
import numpy
import sys
from typing import List

# numpy.set_printoptions(threshold=sys.maxsize)
# correta = create_polynomial_cff(3,2)
# errada = create_polynomial_cff_2(3,2)

# print(correta == errada)

if __name__ == '__main__':
    q = int(sys.argv[1])
    k = int(sys.argv[2])
    start = timer()
    create_cff(q, k)
    end = timer()
    print(end-start)

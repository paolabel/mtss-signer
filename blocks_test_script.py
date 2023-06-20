from mtsssigner.utils.file_and_block_utils import *
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
    file_path = sys.argv[1]
    start = timer()
    get_message_and_blocks_from_file(file_path)
    end = timer()
    print(end-start)

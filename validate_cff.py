from mtsssigner.cff_builder import *
from numpy import logical_or, ndarray
from typing import List, Tuple
import sys
import re
import functools
from multiprocessing import Pool

def get_column(i, cff) -> List[int]:
    return [row[i] for row in cff]

def get_columns(cff):
    columns = []
    for column in range(len(cff[0])):
        columns.append(get_column(column, cff))
    return columns

def convert_bool(list):
    result = []
    for element in list:
        result.append(element == 1)
    return result

def test_cff(q, k):
    d = get_d(q, k)
    cff = create_cff(q, k)
    numpy.set_printoptions(threshold=sys.maxsize)
    assert sorted(set(tuple(map(tuple, cff)))) == sorted(tuple(map(tuple, cff)))
    result = itertools.combinations(range(len(cff)), d)
    columns = get_columns(cff)
    columns = [convert_bool(column) for column in columns]
    columns_str = [str(column) for column in columns]
    
    test_combination = functools.partial(
        test_column_combination,
        columns = columns)

    with Pool(8) as process_pool:
        for result in process_pool.imap(
            test_combination,
            result):
            pass

def test_column_combination(combination, columns: List[List[int]]) -> bool:
    test_column = columns[combination[0]]
    for column in combination[1:]:
        test_column = logical_or(test_column, columns[column])
    for index, column in enumerate(columns):
        if index in combination:
            continue
        if (str(logical_or(test_column, column)) == str(test_column)):
            print(index)
            print(False)

if __name__ == '__main__':
    test_cff(8,2)

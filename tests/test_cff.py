from mtsssigner.cff_builder import *
from numpy import logical_or
from typing import List
import sys

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

def test_cff():
    q = 7
    k = 2
    d = get_d(q, k)
    cff = create_cff(q, k)

    result = itertools.combinations(range(len(cff)), d)
    columns = get_columns(cff)
    columns = [convert_bool(column) for column in columns]
    columns_str = [str(column) for column in columns]
    for combination in result:
        print(combination)
        test_column = columns[combination[0]]
        for column in combination[1:]:
            test_column = logical_or(test_column, columns[column])
        for index, column in enumerate(columns):
            if index in combination:
                continue
            if (str(logical_or(test_column, column)) == str(test_column)):
                print(index)
                assert False

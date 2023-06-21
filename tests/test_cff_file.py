from mtsssigner.cff_builder import *
from mtsssigner.utils.file_and_block_utils import *


def test_1_cff_file():
    original_cff = create_1_cff(4096)
    file_cff = read_cff_from_file(15, 4096, 1) 
    assert len(original_cff) == len(file_cff)
    assert len(original_cff[-1]) == len(file_cff[-1])
    print(original_cff)
    for line in range(len(file_cff)):
        assert original_cff[line] == file_cff[line]
    
def test_2_cff_25_125():
    original_cff = create_cff(5, 3)
    file_cff = read_cff_from_file(25, 125, 2)
    assert len(original_cff) == len(file_cff)
    assert len(original_cff[-1]) == len(file_cff[-1])
    print(original_cff)
    for line in range(len(file_cff)):
        assert original_cff[line] == file_cff[line]

def test_7_cff_64_64():
    original_cff = create_cff(8, 2)
    file_cff = read_cff_from_file(64, 64, 7)
    assert len(original_cff) == len(file_cff)
    assert len(original_cff[-1]) == len(file_cff[-1])
    print(original_cff)
    for line in range(len(file_cff)):
        assert original_cff[line] == file_cff[line]

from multiprocessing import Pool
from Crypto.Hash import SHA256, SHA512, SHA3_256, SHA3_512

S = 4

def test_collision_sha256():
    hash_list = []
    with Pool(8) as process_pool:
            for result in process_pool.imap(__return_sha256,range(2**(S*8))):
                hash_list.append(result)
    assert len(set(hash_list)) == len(hash_list)

def __return_sha256(b: int) -> bytes:
    hash = SHA256.new(__int_to_bytes(b)).digest()
    return hash 

def test_collision_sha512():
    hash_list = []
    with Pool(8) as process_pool:
            for result in process_pool.imap(__return_sha512,range(2**(S*8))):
                hash_list.append(result)
    assert len(set(hash_list)) == len(hash_list)

def __return_sha512(b: int) -> bytes:
    hash = SHA512.new(__int_to_bytes(b)).digest()
    return hash


def test_collision_sha3_256():
    hash_list = []
    with Pool(8) as process_pool:
            for result in process_pool.imap(__return_sha3_256,range(2**(S*8))):
                hash_list.append(result)
    assert len(set(hash_list)) == len(hash_list)

def __return_sha3_256(b: int) -> bytes:
    hash = SHA3_256.new(__int_to_bytes(b)).digest()
    return hash 

def test_collision_sha3_512():
    hash_list = []
    with Pool(8) as process_pool:
            for result in process_pool.imap(__return_sha3_512,range(2**(S*8))):
                hash_list.append(result)
    assert len(set(hash_list)) == len(hash_list)

def __return_sha3_512(b: int) -> bytes:
    hash = SHA3_512.new(__int_to_bytes(b)).digest()
    return hash 
    
# Converts an integer to a bytes object
def __int_to_bytes(number: int) -> bytes:
    return number.to_bytes((len(bin(number)[2:]) + 7) // 8, 'big')
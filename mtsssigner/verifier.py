from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from typing import List, Tuple

from math import sqrt

from cff_builder import create_cff, get_k_from_b_and_q, get_d

DIGEST_SIZE = 256

def verify(message_file_path: str, signature_file_path: str, public_key_file_path: str) -> Tuple[bool, List[int]]:
    with open(message_file_path, "r") as message_file:
        message: str = message_file.read()

    with open(signature_file_path, "rb") as signature_file:
        signature: bytearray = signature_file.read()

    with open(public_key_file_path, "r") as key_file:
        public_key_str: str = key_file.read()

    public_key: RsaKey = RSA.import_key(public_key_str)

    key_modulus = public_key.n.bit_length()

    t = signature[:-int(key_modulus/8)]
    t_hash = SHA256.new(t)
    t_signature = signature[-int(key_modulus/8):]

    try:
        pkcs1_15.new(public_key).verify(t_hash, t_signature)
        print("Signature is valid for T")
    except ValueError:
        print("Signature could not be verified")
        return (False, [])

    message_hash = SHA256.new(message.encode()).digest()
    signature_message_hash = t[-int(DIGEST_SIZE/8):]

    if signature_message_hash == message_hash:
        print("The message was not modified and the signature is valid")
        return (True, [])

    print("The message was modified")

    joined_hashed_tests: bytearray = t[:-int(DIGEST_SIZE/8)]
    hashed_tests: List[bytearray] = [joined_hashed_tests[i:i+int(DIGEST_SIZE/8)] for i in range(0, len(joined_hashed_tests), int(DIGEST_SIZE/8))]

    number_of_tests = len(hashed_tests)
    blocks: list = message.split('\n')
    number_of_blocks = len(blocks)

    cff: list(list) = [[]]
    q: int = int(sqrt(number_of_tests))
    b: int = number_of_blocks
    k: int = get_k_from_b_and_q(b, q)
    d: int = get_d(q, k)
    cff = create_cff(q, k)

    rebuilt_tests: List[str] = list()
    for test in range(number_of_tests):
        concatenation = ""
        for block in range(number_of_blocks):
            if(cff[test][block] == 1):
                concatenation += blocks[block]
        rebuilt_tests.append(concatenation)

    non_modified_blocks: List[int] = list()

    for test in range (len(rebuilt_tests)):
        rebuilt_hashed_test = SHA256.new(rebuilt_tests[test].encode()).digest()
        if (rebuilt_hashed_test == hashed_tests[test]):
            for block in range (number_of_blocks):
                if(cff[test][block] == 1):
                    non_modified_blocks.append(block)

    modified_blocks = [block for block in range(number_of_blocks) if block not in non_modified_blocks]
    result = len(modified_blocks) <= d

    print(f"Resultado: {result}\nBlocos modificados: {modified_blocks}")
    return (result, modified_blocks)

def verify_and_correct(message_file_path: str, signature_file_path: str, public_key_file_path: str) -> Tuple[bool, List[int]]:
    pass

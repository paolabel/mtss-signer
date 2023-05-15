import sys
import subprocess

from mtsssigner.cff_builder import create_cff, get_k_from_b_and_q, create_1_cff
from mtsssigner.utils.file_utils import *

from math import sqrt

from numpy import floor

from getpass import getpass

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

DIGEST_SIZE = 256
DIGEST_SIZE_BYTES = int(DIGEST_SIZE / 8)

# sha256(sha2-256) -> 256 bits de saída -> 32 bytes
# https://crypto.stackexchange.com/questions/95878/does-the-signature-length-of-rs256-depend-on-the-size-of-the-rsa-key-used-for-si
def sign(message_file_path: str, private_key_path: str, max_size_bytes: int = 0, max_modifications: int = 0, k: int = 0) -> bytearray:

    message, blocks= get_message_and_blocks_from_file(message_file_path)
    private_key: RsaKey = __get_private_key_from_file(private_key_path)

    cff: list(list) = [[]]
    cff_dimensions = (0, 0)

    if (max_size_bytes > 0):
        key_modulus = private_key.n.bit_length()
        rsa_signature_output_bytes = key_modulus/8
        message_hash_bytes = DIGEST_SIZE_BYTES
        space_for_tests = max_size_bytes - rsa_signature_output_bytes - message_hash_bytes
        q = int(sqrt(floor(space_for_tests/DIGEST_SIZE_BYTES)))
        b: int = len(blocks)
        k: int = get_k_from_b_and_q(b, q)
        cff = create_cff(q, k)
        cff_dimensions = (q**2, q**k)
    elif (max_modifications == 1):
        cff = create_1_cff(len(blocks))
        cff_dimensions = (len(cff) , len(blocks))
    elif (k > 0):
        pass
    # elif (max_modifications > 0):
    #   b:int = len(blocks)
    #   q: int = get_q_from_error_and_block_number(max_modifications, b)
    #   cff = create_cff(q, get_k_from_b_and_q(b, q))

    tests = list()

    for test in range(cff_dimensions[0]):
        concatenation = bytes()
        for block in range(cff_dimensions[1]):
            if (cff[test][block] == 1):
                concatenation += SHA256.new(blocks[block].encode()).digest()
        tests.append(concatenation)

    signature = bytearray()
    for test in tests:
        test_hash = SHA256.new(test).digest()
        signature += test_hash
    message_hash = SHA256.new(message.encode()).digest()
    signature += message_hash

    t_hash = SHA256.new(signature)
    signed_t = pkcs1_15.new(private_key).sign(t_hash)
    signature += signed_t

    write_signature_to_file(signature, message_file_path)

    return signature

def __get_private_key_from_file(private_key_path: str) -> RsaKey:
    open_pk_command = f"sudo openssl rsa -in {private_key_path}"
    process = subprocess.run(open_pk_command.split(), stdout=subprocess.PIPE)
    openssl_stdout = str(process.stdout)[2:-3]
    private_key_str = __get_correct_private_key_str_from_openssl_stdout(openssl_stdout)
    private_key_password = getpass("Enter private key password again:")
    return RSA.import_key(private_key_str, private_key_password)

def __get_correct_private_key_str_from_openssl_stdout(openssl_stdout: str) -> str:
    lines_key = openssl_stdout.split("\\n")
    private_key_str = lines_key[0] + "\n"
    for line in range(len(lines_key) - 2):
        private_key_str += lines_key[line + 1]
    private_key_str += "\n" + lines_key[-1]
    return private_key_str

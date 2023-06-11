import subprocess
from math import sqrt
from getpass import getpass
from numpy import floor
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from mtsssigner.cff_builder import (create_cff,
                                    get_k_from_n_and_q,
                                    get_q_from_k_and_n,
                                    create_1_cff,
                                    get_d)
from mtsssigner.utils.file_and_block_utils import get_message_and_blocks_from_file
from mtsssigner.utils.prime_utils import is_prime_power
from mtsssigner.signature_scheme import SigScheme
from mtsssigner import logger

# Signs a file using a modification tolerant signature scheme, which
# allows for localization and correction of modifications to the file
# within certain limitations. The number of blocks created from the file
# (their creation depends on the file type) must be a prime power.
# https://crypto.stackexchange.com/questions/95878/does-the-signature-length-
# of-rs256-depend-on-the-size-of-the-rsa-key-used-for-si
def sign(sig_scheme: SigScheme, message_file_path: str, private_key_path: str,
         max_size_bytes: int = 0, k: int = 0) -> bytearray:

    message, blocks= get_message_and_blocks_from_file(message_file_path)
    if not is_prime_power(len(blocks)):
        logger.log_error(("Number of blocks generated must be a prime power "
                          f"to use polynomial CFF (Number of blocks = {len(blocks)}), using 1-CFF"))
        k = 1
    private_key = sig_scheme.get_private_key(private_key_path)

    n: int = len(blocks)

    cff: list(list) = [[]]

    if k == 1:
        cff = create_1_cff(n)
    elif max_size_bytes > 0:
        message_hash_bytes = sig_scheme.digest_size_bytes
        space_for_tests = int(max_size_bytes - sig_scheme.signature_length_bytes - message_hash_bytes)
        if space_for_tests < 0:
            raise ValueError(
                "Desired max signature size is too small for any signature with the supplied key"
            )
        q = int(sqrt(floor(space_for_tests/sig_scheme.digest_size_bytes)))
        k = get_k_from_n_and_q(n, q)
        cff = create_cff(q, k)
    elif k > 1:
        q = get_q_from_k_and_n(k, n)
        cff = create_cff(q, k)
    else:
        raise Exception("Either max size or 'K' value must be provided")

    cff_dimensions = (len(cff), n)
    d = get_d(q, k) if k > 1 else 1
    if k > 1:
        d = get_d(q, k)
        logger.log_signature_parameters(message_file_path, private_key_path, n,
                                sig_scheme, d, len(cff), blocks, q, k, max_size_bytes)
    else:
        d = 1
        logger.log_signature_parameters(message_file_path, private_key_path, n,
                                sig_scheme, d, len(cff), blocks)

    tests = []

    for test in range(cff_dimensions[0]):
        concatenation = bytes()
        for block in range(cff_dimensions[1]):
            if cff[test][block] == 1:
                concatenation += sig_scheme.get_digest(blocks[block])
        tests.append(concatenation)

    signature = bytearray()
    for test in tests:
        test_hash = sig_scheme.get_digest(test)
        signature += test_hash
    message_hash = sig_scheme.get_digest(message)
    signature += message_hash

    signed_t = sig_scheme.sign(private_key, signature)
    signature += signed_t

    return signature

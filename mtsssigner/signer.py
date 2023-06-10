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

# Digest size for the chosen hash function (SHA256)
DIGEST_SIZE = 256
DIGEST_SIZE_BYTES = int(DIGEST_SIZE / 8)

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
    private_key: RsaKey = __get_private_key_from_file(private_key_path)
    key_modulus = private_key.n.bit_length()

    n: int = len(blocks)

    cff: list(list) = [[]]

    if k == 1:
        cff = create_1_cff(n)
    elif max_size_bytes > 0:
        rsa_signature_output_bytes = key_modulus/8
        message_hash_bytes = DIGEST_SIZE_BYTES
        space_for_tests = int(max_size_bytes - rsa_signature_output_bytes - message_hash_bytes)
        if space_for_tests < 0:
            raise ValueError(
                "Desired max signature size is too small for any signature with the supplied key"
            )
        q = int(sqrt(floor(space_for_tests/DIGEST_SIZE_BYTES)))
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
                                key_modulus, d, len(cff), blocks, q, k, max_size_bytes)
    else:
        d = 1
        logger.log_signature_parameters(message_file_path, private_key_path, n,
                                key_modulus, d, len(cff), blocks)

    tests = []

    for test in range(cff_dimensions[0]):
        concatenation = bytes()
        for block in range(cff_dimensions[1]):
            if cff[test][block] == 1:
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

    return signature

# Retrieves a private key from password-protected PEM file using OpenSSL
def __get_private_key_from_file(private_key_path: str) -> RsaKey:
    try:
        with open(private_key_path, "r", encoding="utf=8") as key_file:
            private_key_str: str = key_file.read()
            private_key_lines:str = key_file.readlines()
        if private_key_lines[1] == "Proc-Type: 4,ENCRYPTED":
            private_key_password = getpass("Enter private key password:")
        else:
            private_key_password = None
    except Exception:
        private_key_password = getpass("Enter private key password:")
        open_pk_command = f"openssl rsa -in {private_key_path} -passin pass:{private_key_password}"
        process = subprocess.run(open_pk_command.split(), stdout=subprocess.PIPE, check=True)
        openssl_stdout = str(process.stdout)[2:-3]
        private_key_str = __get_correct_private_key_str_from_openssl_stdout(openssl_stdout)
    return RSA.import_key(private_key_str, private_key_password)

# Returns the correctly formatted string for creating
# a private key object from the OpenSSL process output
def __get_correct_private_key_str_from_openssl_stdout(openssl_stdout: str) -> str:
    lines_key = openssl_stdout.split("\\n")
    private_key_str = lines_key[0] + "\n"
    for line in range(len(lines_key) - 2):
        private_key_str += lines_key[line + 1]
    private_key_str += "\n" + lines_key[-1]
    return private_key_str

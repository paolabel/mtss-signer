from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from typing import List, Tuple

import sys

DIGEST_SIZE = 256

def verify(message_file_path: str, signature_file_path: str, public_key_file_path: str) -> Tuple[bool, List[int]]:
    with open(message_file_path, "r") as message_file:
        message: str = message_file.read()

    with open(signature_file_path, "rb") as signature_file:
        signature: bytearray = signature_file.read()

    with open(public_key_file_path, "r") as key_file:
        public_key_str: str = key_file.read()

    public_key: RsaKey = RSA.import_key(public_key_str)

    key_modulus = len(str(bin(public_key.n))[2:])

    t = signature[:-int(key_modulus/8)]
    print(f"{t.hex()}\nTamanho de T: {len(str(t.hex()))*4}")
    t_hash = SHA256.new(t)
    t_signature = signature[-int(key_modulus/8):]
    print(f"{t_signature.hex()}\nTamanho da assinatura de T: {len(str(t_signature.hex()))*4}")

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

    joined_hashed_tests = t[:-DIGEST_SIZE]
    hashed_tests = [joined_hashed_tests[i:i+DIGEST_SIZE] for i in range(0, len(joined_hashed_tests), DIGEST_SIZE)]

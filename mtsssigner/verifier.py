from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from typing import List, Tuple

DIGEST_SIZE = 256

def verify(message_file_path: str, signature_file_path: str, public_key_file_path: str) -> Tuple[bool, List[int]]:
    with open(message_file_path, "r") as message_file:
        message: str = message_file.read()

    with open(signature_file_path, "rb") as signature_file:
        signature: bytearray = signature_file.read()

    with open(public_key_file_path, "r") as key_file:
        public_key_str: str = key_file.read()

    public_key: RsaKey = RSA.import_key(public_key_str)

    key_n = public_key.n

    t = signature[:key_n]
    t_hash = SHA256.new(t).digest()
    t_signature = signature[-key_n:]

    try:
        pkcs1_15.new(public_key).verify(t_hash, t_signature)
    except ValueError:
        print("Signature could not be verified")
        return (False, [])

    message_hash = SHA256.new(message.encode).digest()
    signature_message_hash = SHA256.new(t[-DIGEST_SIZE:]).digest()

    if signature_message_hash == message_hash:
        print("The message was not modified and the signature is valid")
        return (True, [])

    joined_hashed_tests = t[:-DIGEST_SIZE]
    hashed_tests = [joined_hashed_tests[i:i+DIGEST_SIZE] for i in range(0, len(joined_hashed_tests), DIGEST_SIZE)]

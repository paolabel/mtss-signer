import sys
from timeit import default_timer as timer
import mtsssigner.logger as logger
from mtsssigner.signature_scheme import SigScheme
from mtsssigner.utils.file_and_block_utils import *

# python sign_verify_alpha.py sign/verify algorithm msg key hash signature

if __name__ == '__main__':

    command = sys.argv
    operation = sys.argv[1]
    sig_algorithm = sys.argv[2].lower()
    message_file_path = sys.argv[3]
    key_file_path = sys.argv[4]
    start = timer()
    message, blocks = get_message_and_blocks_from_file(message_file_path)
    content = message.encode()
    try:
        if sig_algorithm == "rsa":
            sig_algorithm = "PKCS#1 v1.5"
            hash_function = sys.argv[5].upper()
            sig_scheme = SigScheme(sig_algorithm, hash_function)
        elif sig_algorithm == "ed25519":
            # For Ed25519, hash function must be SHA512
            sig_scheme = SigScheme(sig_algorithm.capitalize())
        if operation == "sign":
            priv_key = sig_scheme.get_private_key(key_file_path)
            signature = sig_scheme.sign(priv_key, content)
            write_signature_to_file(signature, message_file_path)
        elif operation == "verify":
            with open(sys.argv[6], "rb") as signature_file:
                signature: bytearray = signature_file.read()
            pub_key = sig_scheme.get_public_key(key_file_path)
            result = sig_scheme.verify(pub_key, content, signature)
        else:
            raise ValueError( "Unsupported operation (must be 'sign' or 'verify')")
        end = timer()
        print(end-start)
    except Exception as e:
        print("Error: " + repr(e))
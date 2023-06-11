import sys
from timeit import default_timer as timer
from datetime import timedelta
from typing import List, Tuple
import traceback
from mtsssigner.signer import sign
from mtsssigner.verifier import verify, verify_and_correct
from mtsssigner import logger
from mtsssigner.signature_scheme import SigScheme
from mtsssigner.utils.file_and_block_utils import (get_signature_file_path,
                                                   get_correction_file_path,
                                                   write_correction_to_file,
                                                   write_signature_to_file)

# python mtss_signer.py sign rsa/ed25519 hashfunc messagepath privkeypath -s/-k number 
# python mtss_signer.py verify rsa/ed25519 hashfunc messagepath pubkeypath signaturepath 
# python mtss_signer.py verify-correct rsa/ed25519 hashfunc messagepath pubkeypath signaturepath 

def __print_localization_result(result: Tuple[bool, List[int]]):
    signature_status = "Signature is valid" if result[0] else "Signature could not be verified"
    if result[0]:
        if len(result[1]) == 0:
            localization_status = "message was not modified"
        else:
            localization_status = f"Modified blocks = {result[1]}"
        print(f"\nVerification result: {signature_status}; {localization_status}")
    else:
        print(f"\nVerification result: {signature_status}")

if __name__ == '__main__':

    start = timer()
    command = sys.argv
    operation = sys.argv[1]
    sig_algorithm = sys.argv[2].lower()
    if sig_algorithm.lower() == "rsa":
        sig_algorithm = "PKCS#1 v1.5"
    hash_function = sys.argv[3].upper()
    message_file_path = sys.argv[4]
    key_file_path = sys.argv[5]
    try:
        sig_scheme = SigScheme(sig_algorithm, hash_function)
        logger.log_program_command(command, sig_scheme)
        logger.log_execution_start(operation)
        if operation == "sign":
            flag = sys.argv[6]
            number = int(sys.argv[7])
            if not flag[0] == "-":
                raise ValueError("Invalid argument for flag (must be '-s' or '-k')")
            if flag == "-s":
                signature = sign(sig_scheme, message_file_path, key_file_path, max_size_bytes=number)
                write_signature_to_file(signature, message_file_path)
                print(f"\nSignature written to {get_signature_file_path(message_file_path)}")
            elif flag == "-k":
                signature = sign(sig_scheme, message_file_path, key_file_path, k=number)
                write_signature_to_file(signature, message_file_path)
                print(f"\nSignature written to {get_signature_file_path(message_file_path)}")
            else:
                raise ValueError("Invalid option for sign operation (must be '-s' or '-k')")
        elif operation == "verify":
            signature_file_path = sys.argv[6]
            result = verify(sig_scheme, message_file_path, signature_file_path, key_file_path)
            __print_localization_result(result)
        elif operation == "verify-correct":
            signature_file_path = sys.argv[6]
            result = verify_and_correct(sig_scheme, message_file_path, signature_file_path, key_file_path)
            __print_localization_result(result)
            correction = result[2]
            if correction != "":
                write_correction_to_file(message_file_path, correction)
                print(f"\nCorrection written to {get_correction_file_path(message_file_path)}")
            elif len(result[1]) > 0:
                print(f"\nFile {message_file_path} could not be corrected")
        else:
            raise ValueError( "Unsupported operation (must be 'sign', 'verify' or 'verify-correct')")
        end = timer()
        logger.log_execution_end(timedelta(seconds=end-start))
    except Exception as e:
        logger.log_error(traceback.print_exc)
        print("Error: " + repr(e))

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

def __print_operation_result(enabled: bool, operation: str, message_file_path: str, localization_result: Tuple[bool, List[int]] = None):
    if not enabled:
        return
    if operation == "sign":
        print(f"\nSignature written to {get_signature_file_path(message_file_path)}")
    elif operation == "verify":
        __print_localization_result(localization_result)
    elif operation == "correct":
            print(f"\nCorrection written to {get_correction_file_path(message_file_path)}")

# python mtss_signer.py sign rsa messagepath privkeypath -s/-k number hashfunc
# python mtss_signer.py sign ed25519 messagepath privkeypath -s/-k number
# python mtss_signer.py verify rsa messagepath pubkeypath signaturepath hashfunc
# python mtss_signer.py verify ed25519 messagepath pubkeypath signaturepath
# python mtss_signer.py verify-correct rsa messagepath pubkeypath signaturepath hashfunc
# python mtss_signer.py verify-correct ed25519 messagepath pubkeypath signaturepath hashfunc
# optional --debug or --time-only flag comes last

# If "time only" mode is enabled, the function will print only the total time measurement
# of the execution. Otherwise, it will print the result of the operation
# If debug mode is enabled, the logger will record execution information to the log file.
if __name__ == '__main__':

    command = sys.argv
    operation = sys.argv[1]
    sig_algorithm = sys.argv[2].lower()
    message_file_path = sys.argv[3]
    key_file_path = sys.argv[4]
    logger.enabled = (sys.argv[-1] == "--debug")
    output_time:bool = (sys.argv[-1] == "--time-only")
    print_results: bool = not output_time
    start = timer()
    try:
        if sig_algorithm == "rsa":
            sig_algorithm = "PKCS#1 v1.5"
            hash_function = sys.argv[7].upper() if operation == "sign" else sys.argv[6].upper()
            sig_scheme = SigScheme(sig_algorithm, hash_function)
        elif sig_algorithm == "ed25519":
            # For Ed25519, hash function must be SHA512
            sig_scheme = SigScheme(sig_algorithm.capitalize())
        logger.log_program_command(command, sig_scheme)
        logger.log_execution_start(operation)
        if operation == "sign":
            flag = sys.argv[5]
            number = int(sys.argv[6])
            if not flag[0] == "-":
                raise ValueError("Invalid argument for flag (must be '-s' or '-k')")
            if flag == "-s":
                signature = sign(sig_scheme, message_file_path, key_file_path, max_size_bytes=number)
            elif flag == "-k":
                signature = sign(sig_scheme, message_file_path, key_file_path, k=number)
            else:
                raise ValueError("Invalid option for sign operation (must be '-s' or '-k')")
            write_signature_to_file(signature, message_file_path)
            __print_operation_result(print_results, operation, message_file_path)
        elif operation == "verify":
            signature_file_path = sys.argv[5]
            result = verify(sig_scheme, message_file_path, signature_file_path, key_file_path)
            __print_operation_result(print_results, operation, message_file_path, result)
        elif operation == "verify-correct":
            signature_file_path = sys.argv[5]
            result = verify_and_correct(sig_scheme, message_file_path, signature_file_path, key_file_path)
            __print_operation_result(print_results, "verify", message_file_path, result)
            correction = result[2]
            if correction != "":
                write_correction_to_file(message_file_path, correction)
                __print_operation_result(print_results, operation, message_file_path, result)
            elif len(result[1]) > 0:
                print(f"\nFile {message_file_path} could not be corrected")
        else:
            raise ValueError( "Unsupported operation (must be 'sign', 'verify' or 'verify-correct')")
        end = timer()
        if output_time:
            print(end-start)
        logger.log_execution_end(timedelta(seconds=end-start))
    except Exception as e:
        logger.log_error(traceback.print_exc)
        print("Error: " + repr(e))
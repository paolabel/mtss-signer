import sys
from timeit import default_timer as timer
from datetime import timedelta
from typing import List, Tuple
import traceback
from mtsssigner.signer import sign
from mtsssigner.verifier import verify, verify_and_correct
from mtsssigner import logger
from mtsssigner.utils.file_and_block_utils import (get_signature_file_path,
                                                   get_correction_file_path,
                                                   write_correction_to_file,
                                                   write_signature_to_file)

# python mtss_signer.py sign messagepath privkeypath -s/-k number
# python mtss_signer.py verify messagepath pubkeypath signaturepath
# python mtss_signer.py verify-correct messagepath pubkeypath signaturepath

def __print_localization_result(result: Tuple[bool, List[int]]):
    signature_status = "Signature is valid" if result[0] else "Signature could not be verified"
    if len(result[1]) == 0:
        localization_status = "message was not modified"
    else:
        localization_status = f"Modified blocks = {result[1]}"
    print(f"Verification result: {signature_status}; {localization_status}")

if __name__ == '__main__':

    start = timer()
    command = sys.argv
    operation = sys.argv[1]
    logger.log_program_command(command)
    logger.log_execution_start(operation)
    message_file_path = sys.argv[2]
    key_file_path = sys.argv[3]
    try:
        if operation == "sign":
            flag = sys.argv[4]
            number = int(sys.argv[5])
            if not flag[0] == "-":
                raise ValueError("Invalid argument for flag (must be '-s' or '-k')")
            if flag == "-s":
                signature = sign(message_file_path, key_file_path, max_size_bytes=number)
                write_signature_to_file(signature, message_file_path)
                print(f"Signature written to {get_signature_file_path(message_file_path)}")
            elif flag == "-k":
                sign(message_file_path, key_file_path, k=number)
                print(f"Signature written to {get_signature_file_path(message_file_path)}")
            else:
                raise ValueError("Invalid option for sign operation (must be '-s' or '-k')")
        elif operation == "verify":
            signature_file_path = sys.argv[4]
            result = verify(message_file_path, signature_file_path, key_file_path)
            __print_localization_result(result)
        elif operation == "verify-correct":
            signature_file_path = sys.argv[4]
            result = verify_and_correct(message_file_path, signature_file_path, key_file_path)
            __print_localization_result(result)
            correction = result[2]
            if correction != "":
                write_correction_to_file(message_file_path, correction)
                print(f"Correction written to {get_correction_file_path(message_file_path)}")
            elif len(result[1]) > 0:
                print(f"File {message_file_path} could not be corrected")
        else:
            raise ValueError( "Unsupported operation (must be 'sign', 'verify' or 'verify-correct')")
        end = timer()
        logger.log_execution_end(timedelta(seconds=end-start))
    except Exception as e:
        logger.log_error(traceback.print_exc)
        print("Error: " + repr(e))

import sys
from timeit import default_timer as timer
from datetime import timedelta

from mtsssigner.signer import sign
from mtsssigner.verifier import Verifier
import mtsssigner.logger as logger
from mtsssigner.utils.file_utils import get_signature_file_path, get_correction_file_path

from typing import List, Tuple

# python mtss_signer.py sign messagepath privkeypath -s/-k number
# python mtss_signer.py verify messagepath pubkeypath signaturepath
# python mtss_signer.py verify-correct messagepath pubkeypath signaturepath

def __print_localization_result(result: Tuple[bool, List[int]]):
    signature_status = "Signature is valid" if result[0] == True else "Signature could not be verified"
    localization_status = "message was not modified" if len(result[1]) == 0 else f"modified blocks = {result[1]}"
    print(f"Verification result: {signature_status}, {localization_status}")

if __name__ == '__main__':

    start = timer()
    operation = sys.argv[1]
    logger.log_execution_start(operation)
    message_file_path = sys.argv[2]
    key_file_path = sys.argv[3]
    if operation == "sign":
        flag = sys.argv[4]
        number = int(sys.argv[5])
        if not flag[0] == "-":
            raise ValueError("Invalid argument for flag")
        if flag == "-s":
            sign(message_file_path, key_file_path, max_size_bytes=number)
            print(f"Signature written to {get_signature_file_path(message_file_path)}")
        elif flag == "-k":
            sign(message_file_path, key_file_path, k=number)
            print(f"Signature written to {get_signature_file_path(message_file_path)}")
        else:
            raise ValueError("Invalid option for sign operation")
    elif operation == "verify":
        verifier = Verifier()
        signature_file_path = sys.argv[4]
        result = verifier.verify(message_file_path, signature_file_path, key_file_path)
        __print_localization_result(result)
    elif operation == "verify-correct":
        verifier = Verifier()
        signature_file_path = sys.argv[4]
        result = verifier.verify_and_correct(message_file_path, signature_file_path, key_file_path)
        __print_localization_result(result)
        print(f"Correction written to {get_correction_file_path(message_file_path, message_file_path[-3:])}")
    end = timer()
    logger.log_execution_end(timedelta(seconds=end-start))

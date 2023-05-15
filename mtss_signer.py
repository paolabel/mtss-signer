import sys
from timeit import default_timer as timer
from datetime import timedelta

from mtsssigner.signer import sign
from mtsssigner.verifier import Verifier

# python mtss_signer.py sign messagepath privkeypath -s/-k number
# python mtss_signer.py verify messagepath pubkeypath signaturepath
# python mtss_signer.py verify-correct messagepath pubkeypath signaturepath
if __name__ == '__main__':

    start = timer()

    operation = sys.argv[1]
    message_file_path = sys.argv[2]
    key_file_path = sys.argv[3]
    if operation == "sign":
        flag = sys.argv[4]
        number = int(sys.argv[5])
        if not flag[0] == "-":
            raise ValueError("Invalid argument for flag")
        if flag == "-s":
            sign(message_file_path, key_file_path, max_size_bytes=number)
        elif flag == "-k":
            sign(message_file_path, key_file_path, max_modifications=number)
        else:
            raise ValueError("Invalid option for sign operation")
    elif operation == "verify":
        verifier = Verifier()
        signature_file_path = sys.argv[4]
        verifier.verify(message_file_path, signature_file_path, key_file_path)
    elif operation == "verify-correct":
        verifier = Verifier()
        signature_file_path = sys.argv[4]
        verifier.verify_and_correct(message_file_path, signature_file_path, key_file_path)

    end = timer()
    print(f"Elapsed time: {timedelta(seconds=end-start)}")

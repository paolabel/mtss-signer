import sys

from signer import sign
from verifier import verify

# python mtss_signer.py sign messagepath privkeypath -s/-m number
# python mtss_signer.py verify messagepath pubkeypath signaturepath
if __name__ == '__main__':
    operation = sys.argv[1]
    message_file_path = sys.argv[2]
    key_file_path = sys.argv[3]
    if operation == "sign":
        flag = sys.argv[4]
        number = int(sys.argv[5])
        if not flag[0] == "-":
            raise ValueError("Invalid argument for flag")
        if flag == "-s":
            sign(message_file_path, key_file_path, max_tests= number)
        elif flag == "-m":
            sign(message_file_path, key_file_path, max_modifications= number)
        else:
            raise ValueError("Invalid option for sign operation")
    elif operation == "verify":
        signature_file_path = sys.argv[4]
        verify(message_file_path, signature_file_path, key_file_path)
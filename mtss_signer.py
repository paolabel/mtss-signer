import sys
from timeit import default_timer as timer
from datetime import timedelta

from mtsssigner.signer import sign
from mtsssigner.verifier import Verifier
import mtsssigner.logger as logger
from mtsssigner.utils.file_and_block_utils import get_signature_file_path, get_correction_file_path, write_correction_to_file, write_signature_to_file

from typing import List, Tuple

import traceback

# python mtss_signer.py sign messagepath privkeypath -s/-k number
# python mtss_signer.py verify messagepath pubkeypath signaturepath
# python mtss_signer.py verify-correct messagepath pubkeypath signaturepath

def __print_localization_result(result: Tuple[bool, List[int]]):
    signature_status = "Signature is valid" if result[0] == True else "Signature could not be verified"
    localization_status = "message was not modified" if len(result[1]) == 0 else f"Modified blocks = {result[1]}"
    print(f"Verification result: {signature_status}; {localization_status}")

if __name__ == '__main__':
    
    # prompt = (
    #     "Para assinar: 'sign <path do arquivo> <path da chave privada> <flag> <valor inteiro>'\n"
    #     "- Opções de flag: -s (definir tamanho máximo em bytes do arquivo da assinatura)\n"
    #     "                  -k (Valores maiores = menor assinatura, valores menores = maior número de modificações possíveis, k >= 2)\n"
    #     "Para verificar assinatura:\n"
    #     "- Apenas com localização de erros: 'verify <path do arquivo a verificar> <path da chave pública> <path da assinatura>'\n"
    #     "- Com localização e correção de erros: 'verify-correct <path do arquivo a verificar> <path da chave pública> <path da assinatura>'\n"
    # )

    # commands = input(prompt).split(" ")
    # print(commands)

    start = timer()
    command = sys.argv
    operation = sys.argv[1]
    logger.log_program_input(command)
    logger.log_execution_start(operation)
    message_file_path = sys.argv[2]
    key_file_path = sys.argv[3]
    try:
        if operation == "sign":
            flag = sys.argv[4]
            number = int(sys.argv[5])
            if not flag[0] == "-":
                raise ValueError("Error: Invalid argument for flag")
            if flag == "-s":
                signature = sign(message_file_path, key_file_path, max_size_bytes=number)
                write_signature_to_file(signature, message_file_path)
                print(f"Signature written to {get_signature_file_path(message_file_path)}")
            elif flag == "-k":
                sign(message_file_path, key_file_path, k=number)
                print(f"Signature written to {get_signature_file_path(message_file_path)}")
            else:
                raise ValueError("Error: Invalid option for sign operation")
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
            correction = result[2]
            if correction != "":
                write_correction_to_file(message_file_path, correction)
                print(f"Correction written to {get_correction_file_path(message_file_path)}")
            elif len(result[1]) > 0:
                print(f"File {message_file_path} could not be corrected")
        end = timer()
        logger.log_execution_end(timedelta(seconds=end-start))
    except Exception as e:
        logger.log_error(traceback.print_exc)
        print("Error: " + repr(e))

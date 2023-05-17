from datetime import datetime
from datetime import timedelta
from typing import List
from numpy import sqrt, floor

LOG_FILE_PATH="./logs.txt"
DIGEST_SIZE_BYTES = 256/8

def log_correction_progress(b: int):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    __write_to_log_file(f"Current time = {current_time}, correction operation number = {b}\n")

def log_execution_start(operation: str):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    log_content = ("##############################\n"
                  f"Start time = {current_time}\n"
                  f"Operation: {operation}\n")
    __write_to_log_file(log_content)
    
def log_error(error: str):
    __write_to_log_file(f"Error: {error}\n")

def log_execution_end(elapsed_time: timedelta):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    __write_to_log_file((f"End time = {current_time}\n"
                         f"Elapsed time: {elapsed_time}\n"))

# TODO mostrar quando número de blocos foi arredondado para combinar com K
# TODO mostrar quando k resultante foi incompatível com tamanho+blocos compatível
def log_signature_parameters(signed_file: str, private_key_file: str, n:int, key_modulus:int, q:int, d:int, k:int, t:int, max_size_bytes = 0):
    log_content = f"Signed file = {signed_file}; Private key file = {private_key_file}\n"
    log_content += f"Number of blocks = {n}; Private key modulus = {key_modulus}\n"
    if max_size_bytes > 0:
        rsa_signature_output_bytes = key_modulus/8
        message_hash_bytes = DIGEST_SIZE_BYTES
        space_for_tests = int(max_size_bytes - rsa_signature_output_bytes - message_hash_bytes)
        log_content += f"Supplied max size for signature (in bytes) = {max_size_bytes}\n"
        log_content += f"Bytes available for hashed tests = {space_for_tests}\n"
        log_content += f"Unrounded number of tests available = {(space_for_tests/DIGEST_SIZE_BYTES)}\n"
    else:
        log_content += f"Supplied k = {k}\n"
    log_content += f"Resulting CFF = {d}-CFF({t}, {n}), q = {q}, k = {k}\n"
    __write_to_log_file(log_content)

def log_nonmodified_verification_result(verified_file: str, public_key_file: str, result: bool):
    log_content = f"Verified file = {verified_file}; Public key file = {public_key_file}\n"
    signature_status = "Valid" if result else "Invalid"
    log_content += f"Signature status: {signature_status}"
    if result:
        log_content += f"The message was not modified"
    __write_to_log_file(log_content)

def log_localization_result(verified_file: str, public_key_file: str, n:int, t:int, d: int, q:int, k:int, result: bool, modified_blocks: List[int], modified_blocks_content: List[str]):
    log_content = f"Verified file = {verified_file}; Public key file = {public_key_file}\n"
    log_content += f"Number of blocks = {n}, Number of tests = {t}, Max modifications = {d}\n"
    log_content += f"Resulting CFF = {d}-CFF({t}, {n}), q = {q}, k = {k}\n"
    signature_status = "Valid" if result else "Invalid"
    log_content += f"Signature status: {signature_status}; Modified_blocks = {modified_blocks}; Modified_content = {modified_blocks_content}\n"
    localization_result = "complete" if len(modified_blocks) <= d else "incorrect (too many modifications)\n"
    log_content += f"Localization result: {localization_result}\n"
    __write_to_log_file(log_content)

def log_correction_parameters(s: int, process_pool_size: int):
    __write_to_log_file((f"Max ASCII (1 byte) characters to correct per block = {s}\n"
                         f"Available parallel processes to realize the correction: {process_pool_size}\n"))

def log_block_correction(block_number: int, correction: str = ""):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if block_number > -1:
        __write_to_log_file(f"({current_time}) Block {block_number} was corrected, correction value = '{correction}'\n")
    else:
        __write_to_log_file(f"{current_time} : No block could be corrected\n")

def log_collision(block_number: int, collision: str):
    __write_to_log_file(f"Collision found for block {block_number}, collision value = '{collision}'\n")

def __write_to_log_file(content: str):
    log_file = open(LOG_FILE_PATH, "a")
    log_file.write(content)
    log_file.close()

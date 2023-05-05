from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from multiprocessing import Pool

import functools

from typing import List, Tuple

from math import sqrt

from cff_builder import create_cff, get_k_from_b_and_q, get_d

DIGEST_SIZE = 256
MAX_CORRECTABLE_BLOCK_LEN_CHARACTERS = 3

class Verifier:

    cff: List[List[int]] = [[]]
    message: str
    blocks: List[str]
    hashed_tests: List[bytearray]
    corrected = dict()

    def verify(self, message_file_path: str, signature_file_path: str, public_key_file_path: str) -> Tuple[bool, List[int]]:
        with open(message_file_path, "r") as message_file:
            self.message = message_file.read()

        with open(signature_file_path, "rb") as signature_file:
            signature: bytearray = signature_file.read()

        with open(public_key_file_path, "r") as key_file:
            public_key_str: str = key_file.read()

        public_key: RsaKey = RSA.import_key(public_key_str)

        key_modulus = public_key.n.bit_length()

        t = signature[:-int(key_modulus/8)]
        t_hash = SHA256.new(t)
        t_signature = signature[-int(key_modulus/8):]

        try:
            pkcs1_15.new(public_key).verify(t_hash, t_signature)
        except ValueError:
            print("Signature could not be verified")
            return (False, [])

        message_hash = SHA256.new(self.message.encode()).digest()
        signature_message_hash = t[-int(DIGEST_SIZE/8):]

        if signature_message_hash == message_hash:
            print("The message was not modified and the signature is valid")
            return (True, [])

        joined_hashed_tests: bytearray = t[:-int(DIGEST_SIZE/8)]
        self.hashed_tests: List[bytearray] = [joined_hashed_tests[i:i+int(DIGEST_SIZE/8)] for i in range(0, len(joined_hashed_tests), int(DIGEST_SIZE/8))]

        number_of_tests = len(self.hashed_tests)
        self.blocks: list = self.message.split('\n')
        number_of_blocks = len(self.blocks)

        q: int = int(sqrt(number_of_tests))
        b: int = number_of_blocks
        k: int = get_k_from_b_and_q(b, q)
        d: int = get_d(q, k)
        self.cff = create_cff(q, k)
        rebuilt_tests: List[str] = list()
        for test in range(number_of_tests):
            concatenation = bytes()
            for block in range(number_of_blocks):
                if(self.cff[test][block] == 1):
                    concatenation += SHA256.new(self.blocks[block].encode()).digest()
            rebuilt_tests.append(concatenation)

        non_modified_blocks: List[int] = list()

        for test in range (len(rebuilt_tests)):
            rebuilt_hashed_test = SHA256.new(rebuilt_tests[test]).digest()
            if (rebuilt_hashed_test == self.hashed_tests[test]):
                for block in range (number_of_blocks):
                    if(self.cff[test][block] == 1):
                        non_modified_blocks.append(block)

        modified_blocks = [block for block in range(number_of_blocks) if block not in non_modified_blocks]
        result = len(modified_blocks) <= d

        print(f"Resultado: {result}\nBlocos modificados: {modified_blocks}")
        return (result, modified_blocks)

    # retorna a mensagem corrigida em um arquivo
    def verify_and_correct(self, message_file_path: str, signature_file_path: str, public_key_file_path: str) -> Tuple[bool, List[int]]:
        verification_result = self.verify(message_file_path, signature_file_path, public_key_file_path)
        if verification_result[0] == False or verification_result[1] == []:
            return verification_result
        for k in verification_result[1]:
            i_rows = list()
            modified_blocks_minus_k = set(verification_result[1]) - {k}
            for i in range(len(self.cff)):
                if self.cff[i][k] == 1:
                    i_rows.append(i)
                    for j in modified_blocks_minus_k:
                        if self.cff[i][j] == 1:
                            i_rows.pop()
                            break
            i = i_rows[0]
            self.corrected[k] = False
            find_correct_b = functools.partial(return_if_correct_b, self=self, i=i, k=k)
            process_pool_size = available_cpu_count()
            print(f"Limite de caracteres por linha para a correção: {MAX_CORRECTABLE_BLOCK_LEN_CHARACTERS}")
            print(f"Processos paralelos: {process_pool_size}")
            with Pool(process_pool_size) as process_pool:
                for result in process_pool.imap(
                    find_correct_b,
                    range(2**(MAX_CORRECTABLE_BLOCK_LEN_CHARACTERS*8))):
                    if result != None:
                        if result[0] == True:
                            self.corrected[k] = True
                            self.blocks[k] = (int_to_bytes(result[1])).decode("utf-8")
                            print(f"Bloco {k} foi corrigido")
                            break
        if any(correction == True for correction in self.corrected.values()):
            correction_file_path = message_file_path.rsplit(".", 1)[0] + "_corrected.txt"
            with open(correction_file_path, "w") as correction_file:
                correction_file.write("\n".join(self.blocks))
        else:
            print("Nenhum bloco foi corrigido")
        return verification_result

def return_if_correct_b(b: int, verifier: Verifier, i: int, k: int) -> Tuple[bool, int] | None:
    hash_k = SHA256.new(int_to_bytes(b)).digest()
    concatenation = bytes()
    for block in range(len(verifier.cff[i])):
        if verifier.cff[i][block] == 1:
            if block != k:
                concatenation += SHA256.new(verifier.blocks[block].encode()).digest()
            else:
                concatenation += hash_k
    rebuilt_corrected_test = SHA256.new(concatenation).digest()
    if rebuilt_corrected_test == verifier.hashed_tests[i]:
        if verifier.corrected[k] == False:
            return (True, b)
        else:
            print("Houve colisão")
            return (False, b)

def int_to_bytes(number: int):
    return number.to_bytes((len(bin(number)[2:]) + 7) // 8, 'big')

# https://stackoverflow.com/questions/1006289/how-to-find-out-the-number-of-cpus-using-python
def available_cpu_count():
    """ Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program"""

    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        import re
        m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                      open('/proc/self/status').read())
        if m:
            res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
            if res > 0:
                return res
    except IOError:
        pass

    # Python 2.6+
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # Linux
    try:
        res = open('/proc/cpuinfo').read().count('processor\t:')

        if res > 0:
            return res
    except IOError:
        pass

    raise Exception('Can not determine number of CPUs on this system')

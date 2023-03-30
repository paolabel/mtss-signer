def verify(message_file_path: str, signature_file_path: str, public_key_file_path: str):
    with open(message_file_path, "r") as message_file:
        message: str = message_file.read()

    with open(signature_file_path, "rb") as signature_file:
        signature: bytearray = signature_file.read()

    with open(public_key_file_path, "r") as key_file:
        public_key_str: str = key_file.read()
    pass
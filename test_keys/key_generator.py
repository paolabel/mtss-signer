import sys
from getpass import getpass
from Crypto.PublicKey import RSA, ECC

# Generates PKCS#1 RSA private/public key pair and writes them 
# to {key_path}_priv.pem and {key_path}_pub.pem respectively
def __gen_rsa_keypair(modulus: int, key_path:str):
    key = RSA.generate(modulus)
    private_key_password = getpass(
        "Enter desired private key password (press Enter for no password):"
    )
    if private_key_password == "":
        private_key = key.export_key(pkcs=1)
    else:
        private_key = key.export_key(passphrase=private_key_password,pkcs=1)
    with open(key_path + "_priv.pem", "wb") as priv_key_file:
        priv_key_file.write(private_key)

    public_key = key.publickey().export_key()
    with open(key_path + "_pub.pem", "wb") as pub_key_file:
        pub_key_file.write(public_key)

# Generates PKCS#8 Ed25519 private/public key pair and writes them 
# to {key_path}_priv.pem and {key_path}_pub.pem respectively
def __gen_ed22519_keypair(key_path:str):
    key = ECC.generate(curve="ed25519")
    private_key_password = getpass(
        "Enter desired private key password (press Enter for no password):"
    )
    if private_key_password == "":
        private_key = key.export_key(format="PEM", use_pkcs8=True)
    else:
        private_key = key.export_key(
            format="PEM",
            use_pkcs8=True,
            passphrase=private_key_password,
            protection="PBKDF2WithHMAC-SHA1AndAES128-CBC"
        )
    with open(key_path + "_priv.pem", "w") as priv_key_file:
        priv_key_file.write(private_key)
        
    public_key = key.public_key().export_key(format="PEM")
    with open(key_path + "_pub.pem", "w") as pub_key_file:
        pub_key_file.write(public_key)

# python key_generator.py rsa {key name} {modulus}
# python key_generator.py ed25519 {key name}
if __name__ == '__main__':
    algorithm = sys.argv[1].lower()
    key_name = sys.argv[2]
    if algorithm == "rsa":
        key_modulus = int(sys.argv[3])
        __gen_rsa_keypair(key_modulus, key_name)
    elif algorithm == "ed25519":
        __gen_ed22519_keypair(key_name)
    else:
        print("Unspported opperation (must be 'rsa' or 'ed25519')")

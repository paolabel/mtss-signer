Dependências: Python 3.10, pycryptodome, galois, pytest, sympy

Por enquanto só há opção de assinar usando esquema PKCS#1 v1.5 com SHA256 e de criar a assinatura de modo detached

Gerar chaves RSA PKCS#1 em formato PEM com OpenSSL-1.1:
- Chave privada sem senha: ```openssl-1.1 genrsa -out {nome do arquivo}.pem {modulus da chave}```
- Chave privada com senha: ```openssl-1.1 genrsa -aes128 -out {nome do arquivo}.pem {modulus da chave}```
- Chave pública: ```openssl-1.1 rsa -in {nome do arquivo da chave privada}.pem -outform PEM -pubout -out {nome do arquivo p/ chave pública}.pem```

Gerar chaves RSA PKCS#1 em formato PEM com script próprio:

- ```python test_keys/key_generator.py rsa {nome dos arquivos} {modulus da chave}```

Gerar chaves Ed25519 PKCS#8 em formato PEM com script próprio:

- ```python test_keys/key_generator.py ed25519 {nome dos arquivos}```


Gerar assinatura detached com openssl:

```openssl dgst -sha256 -sign {arquivo da chave privada} -out {nome do arquivo da assinatura} {arquivo pra assinar}```

```openssl base64 -in {arquivo da assinatura em binário} -out {arquivo da assinatura em base64}``` (p/ gerar base64 da assinatura)

Verificar assinatura detached com openssl:

```openssl dgst -sha256 -verify {arquivo da chave pública} -signature {arquivo da assinatura em binário} {arquivo assinado}```

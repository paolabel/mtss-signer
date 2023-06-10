Dependências: Python 3.10, pycryptodome, galois, pytest, sympy

Por enquanto só há opção de assinar usando esquema PKCS#1 v1.5 com SHA256 e de criar a assinatura de modo detached

Considerar criar script para criação de chaves ao invés de depender da versão do OpenSSL

A chave privada sem senha pode ser criada com o comando ```openssl-1.1 genrsa -out {nome do arquivo}.pem {modulus da chave}``
A chave privada com senha pode ser criada com o comando ```openssl-1.1 genrsa -aes128 -out {nome do arquivo}.pem {modulus da chave}```

A chave pública pode ser criada com o comando```openssl-1.1 rsa -in {nome do arquivo da chave privada}.pem -outform PEM -pubout -out -out {nome do arquivo p/ chave pública}.pem```

Gerar assinatura detached com openssl:

```openssl dgst -sha256 -sign {arquivo da chave privada} -out {nome do arquivo da assinatura} {arquivo pra assinar}```

```openssl base64 -in {arquivo da assinatura em binário} -out {arquivo da assinatura em base64}``` (p/ gerar base64 da assinatura)

Verificar assinatura detached com openssl:

```openssl dgst -sha256 -verify {arquivo da chave pública} -signature {arquivo da assinatura em binário} {arquivo assinado}```

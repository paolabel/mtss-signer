Dependências: Python 3.10, pycryptodome, galois, pytest, sympy

Por enquanto só há opção de assinar usando esquema PKCS#1 v1.5 com SHA256 e de criar a assinatura de modo detached

Considerar criar script para criação de chaves ao invés de depender da versão do OpenSSL

A chave privada pode ser criada  com o comando ```sudo openssl-1.1 genrsa -des3 -out {nome do arquivo}.pem {modulus da chave}```

A chave pública pode ser criada com o comando```sudo openssl-1.1 rsa -in {nome do arquivo}.pem -outform PEM -pubout -out {nome do arquivo}.pem```

Gerar assinatura detached com openssl:

```openssl dgst -sha256 -sign {arquivo da chave privada} -out {nome do arquivo da assinatura} {arquivo pra assinar}```

```openssl base64 -in {arquivo da assinatura em binário} -out {arquivo da assinatura em base64}``` (p/ gerar base64 da assinatura)

Verificar assinatura detached com openssl:

```openssl dgst -sha256 -verify {arquivo da chave pública} -signature {arquivo da assinatura em binário} {arquivo assinado}```

Parâmetros de assinatura opcionais planejados:

    - Número de erros/modificações máximo permitido
    - Tamanho máximo da assinatura (depende do tamanho da chave)

Por enquanto só há opção de assinar usando esquema PKCS#1 v1.5 com SHA256

Falta assinar XML

Dependências: pycrypto, galois, numpy

A chave privada pode ser criada com o comando ```sudo openssl genrsa -des3 -out {nome do arquivo}.pem {modulus da chave}```

A chave pública pode ser criada com o comando```sudo openssl rsa -in {nome do arquivo}.pem -outform PEM -pubout -out {nome do arquivo}.pem```

    - Ambos os comandos colocam os arquivos com as chaves na home do usuário
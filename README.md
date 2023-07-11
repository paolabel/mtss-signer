

# Descrição

O objetivo da aplicação é o de gerar e verificar assinaturas seguindo o esquema MTSS, é possível localizar modificações feitas no documento assinado até certo ponto. Para isso, o arquivo é separado em blocos, e até ```d``` blocos podem ser modificados conforme a estrutura gerada para a assinatura. O funcionamento do esquema é descrito em detalhes no trabalho ...
# Utilização

Dependências: Python 3.10, pycryptodome, galois, pytest, sympy

## Geração de chaves

A aplicação aceita a utilização de chaves PKCS#1 ou Ed25519, e novas chaves podem ser geradas com os comandos abaixo. O resultado do script será um par de arquivos de nome ```{caminho das chaves}_priv.pem``` e ```{caminho das chaves}_pub.pem```, para a chave privada e pública respectivamente. Caso o caminho desejado para os arquivos não seja especificado, as chaves serão salvas na pasta ```test_keys```. Caso se deseje criptografar a chave privada, será dada a opção de inserir a senha durante a execução.

- Geração de chaves PKCS#1 

    - ```python test_keys/key_generator.py rsa {caminho das chaves} {modulus da chave}```

- Geração de chaves Ed25519 

    - ```python test_keys/key_generator.py ed25519 {caminho das chaves}```

## Geração de assinatura

A aplicação gera assinaturas detached, com a opção de se assinar utilizando os esquemas tradicionais PKCS#1 v1.5 (RSA) ou Ed25519. Os hashes para a assinatura podem ser criados a partir das funções SHA256, SHA512, SHA3-256 ou SHA3-512. São aceitos para assinar arquivos de texto (extensão ```.txt```) ou XML.

- ```python mtss_signer.py sign {alg. assinatura} {caminho do arquivo} {caminho da chave privada} {flag} {valor inteiro} {função hash}```

O resultado do algoritmo, se bem sucedido, será uma assinatura detached de nome ```{caminho do arquivo}_sig.mts```.

- Algoritmos de assinatura: ```rsa``` ou ```ed25519```
- Flag: ```-k``` ou ```-s```
    - Flag ```s``` define o tamanho máximo da assinatura em bytes (o valor precisa ser compatível com a estrutura gerada para a assinatura e os algoritmos de assinatura e hash utilizados)
    - Flag ```k``` pode receber valores a partir de 1. Para k=1, será gerada uma assinatura que detecta até 1 modificação. A partir desse valor, números maiores para k terão uma maior compressão de assinatura em relação ao número de blocos, mas menos erros detectáveis em número e proporção. O valor de k precisa ser compatível com o número de blocos (```n```) gerados para o documento a ser assinado, já que n é necessariamente uma potência de primo elevado por k.
- Funções de hash: ```sha256```, ```sha512```, ```sha3-256```, ```sha3-512```

## Verificação de assinatura com localização de modificações

- ```python mtss_signer.py verify {alg. assinatura} {caminho do arquivo} {caminho da chave pública} {caminho da assinatura} {função hash}```

Se bem sucedido, o resultado será a exibição de quais índices de blocos foram modificados.

## Verificação de assinatura com localização e correção de modificações

- ```python mtss_signer.py verify-correct {alg. assinatura} {caminho do arquivo} {caminho da chave pública} {caminho da assinatura} {função hash}```

Se bem sucedido, o resultado será a exibição de quais índices de blocos foram modificados e um arquivo de nome ```{caminho do arquivo}_corrected.{extensão original do arquivo}``` que conterá a correção.

## Opções adicionais

No final dos comandos, se for inserida a flag ```--debug```, a aplicação registrará dados sobre a execução no arquivo ```logs.txt```, como quais os blocos e CFFs gerados para o documento, além de dados de medição de tempo. Para realizar medições de tempo a partir da saída dos algoritmos, ao invés de serem exibidos os resultados da execução, a flag ```--time-only``` pode ser utilizada para que a saída no terminal seja apenas o tempo de execução em segundos. As opções são mutuamente exclusivas, para o registro de informações de debug não interferir nos dados da medição de tempo mais precisa.
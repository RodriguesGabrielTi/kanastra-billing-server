# kanastra Billing Server
Este projeto foi desenvolvido para automatizar o processamento de arquivos CSV, a geração de boletos bancários e o envio de e-mails, utilizando arquitetura baseada em DDD (Domain-Driven Design).

Este projeto é uma API para processar arquivos CSV e gerar boletos de cobrança.

## Requisitos

- Docker
- Docker Compose

## Como rodar o projeto

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/kanastra-billing-server.git
    cd kanastra-billing-server
    ```

2. Clone o repositório:
    ```bash
    docker-compose up --build
    ```
   
3. A API estará disponível em http://localhost:8000.

## Testes

Para rodar os testes, execute:
```bash 
echo $PYTHONPATH
export PYTHONPATH=$(pwd)/app
poetry install
poetry run pytest
```

## Endpoints
- POST /upload: Envie um arquivo CSV para processamento.

## Exemplo de CSV

```csv
name,governmentId,email,debtAmount,debtDueDate,debtId
John Doe,11111111111,johndoe@kanastra.com.br,1000000.00,2022-10-12,1adb6ccf-ff16-467f-bea7-5f05d494280f
```

## Verificar se os dados foram cadastrados:

Considerando que o Container está rodando, rode o seguinte comando para entrar na maquina do mongo:

```bash
    docker exec -it kanastra_mongo mongosh -u mongo_user -p mongo_password --authenticationDatabase admin
```

Selecione a base
```bash
    use kanastra_billing
```

Contabilize a quantidade de documentos da collection
```bash
    db.billing_debts.countDocuments()
```

Liste os primeiros 5 arquivos
```bash
   db.debts.find().limit(5);
```
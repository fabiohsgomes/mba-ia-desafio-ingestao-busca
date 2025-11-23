# Desafio MBA Engenharia de Software com IA - Full Cycle

Após clonar o projeto, execute os seguintes passos na raíz do projeto:

1. Criar ambiente virutal python:
    ```bash
    python3 -m venv venv
    ```

2. Iniciar o ambiente virtual:
    ```bash
    source venv/bin/activate
    ```

3. Instalar as dependências do projeto:
    ```bash
    pip install -r requirements.txt
    ```

## Executando o projeto

1. Subindo container do banco de dados Postgree + Vector para a ingestão do documento:
    ```bash
    docker compose up -d
    ```

2. Realizando a ingestão do documento "documento.pdf", localizado na raiz do projeto:
    ```bash
    python src/ingest.py

    # ou 
    python3 src/ingest.py
    ```

3. Executando o chat:
    ```bash
    python src/chat.py

    # ou
    python3 src/chat.py
    ```
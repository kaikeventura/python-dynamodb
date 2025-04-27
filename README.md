# Projeto de Teste com DynamoDB e LocalStack

Este é um projeto de exemplo que utiliza o **DynamoDB** e o **LocalStack** para simulação de um banco de dados NoSQL local para testes. O projeto inclui operações básicas como criação, leitura e deleção de itens na tabela do DynamoDB, utilizando a AWS SDK para Python (Boto3).

## Requisitos

- Python 3.12
- Docker (para rodar o LocalStack)

## Configuração do Ambiente

### 1. Criar um Ambiente Virtual

Para começar, crie um ambiente virtual Python para isolar as dependências do projeto.

No terminal, execute o comando abaixo para criar o ambiente virtual:

```bash
python -m venv venv
```

### 2. Ativar o Ambiente Virtual
No Linux:
```bash
source .venv/bin/activate
```

No Windows:
```bash
venv\Scripts\activate
```

### 3. Instalar as Dependências
Após ativar o ambiente virtual, instale as dependências necessárias com o seguinte comando:
```bash
pip install -r requirements.txt
```

### 4. Rodar o LocalStack com Docker Compose
Para rodar o LocalStack e simular os serviços da AWS localmente, você pode utilizar o Docker Compose. Caso já tenha o Docker instalado, execute o comando:
```bash
docker-compose up -d
```

---
title: Documentação do Backend
slug: /backend.md
---

# Backend

Este documento fornece informações detalhadas sobre o backend construído utilizando FastAPI, SQLAlchemy e PyTorch para modelagem preditiva e gerenciamento de banco de dados. O backend conecta-se a um banco de dados PostgreSQL e fornece vários endpoints para gerenciar previsões, verificações de saúde e geração de dados simulados.

:::warning
Esta é a primeira versão do backend do projeto, atualizações e melhorias serão implementadas em sprints futuras
:::
    
## Configuração do Projeto

Para executar este backend, você precisa ter o Python instalado em sua máquina, juntamente com as dependências necessárias. O backend utiliza o FastAPI para construção da API, o SQLAlchemy para ORM (Mapeamento Objeto-Relacional) e o PyTorch para inferência de modelo de machine learning.

## Dependências

Aqui está uma lista das principais bibliotecas e pacotes usados neste backend:

- **FastAPI**: Um framework web moderno e rápido para construção de APIs com Python 3.6+.
- **SQLAlchemy**: Um toolkit SQL e biblioteca ORM para Python.
- **PyTorch**: Uma biblioteca open-source de machine learning para Python, usada aqui para carregar e usar um modelo de rede neural treinado.
- **Pandas**: Uma biblioteca de manipulação e análise de dados usada para trabalhar com arquivos CSV.
- **PostgreSQL**: O sistema de banco de dados utilizado para armazenar os registros de previsões.

Para instalar os pacotes Python necessários, use o seguinte comando:

```bash
pip install fastapi sqlalchemy torch pandas psycopg2-binary
```

## Configuração do Banco de Dados

A aplicação utiliza PostgreSQL como seu banco de dados. A conexão é configurada utilizando o SQLAlchemy. A string de conexão é definida da seguinte forma:

```bash
DATABASE_URL = "postgresql://postgres:SENHA@localhost:5432/fillmore"
```

### Sessão de Banco de Dados

Uma sessão de banco de dados é criada usando a função sessionmaker do SQLAlchemy. Esta sessão é utilizada em vários endpoints para interagir com o banco de dados.

```bash
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## Modelos SQLAlchemy

### Modelo Prediction

O modelo `Prediction` representa a estrutura da tabela teste no banco de dados, que é usada para armazenar previsões e as features associadas.

```python
class Prediction(Base):
    __tablename__ = "teste"

    ID = Column(String, primary_key=True, index=True)
    KNR = Column(String)
    Date = Column(String)
    Feature1 = Column(Float)
    Feature2 = Column(Float)
    Feature3 = Column(Float)
    Prediction_result = Column(Integer)
    Real_result = Column(Integer)
```

A tabela é criada automaticamente no banco de dados, caso ainda não exista:

```bash
Base.metadata.create_all(bind=engine)
``` 
## Endpoints da API

### Endpoint Root

O endpoint root fornece uma mensagem simples de "Hello World" para verificar se o servidor está em funcionamento.

- Endpoint: `GET /`
- Resposta:
    ```json
    {
    "message": "Hello World"
    }
    ```

### Endpoint de Dados Simulados

Este endpoint gera dados simulados e os insere na tabela teste.

- Endpoint: `POST /mock`
- Parâmetros:
    - `num_records (int, default=10)`: O número de registros simulados a serem gerados.
- Resposta:
    ```json
    {
    "message": "{num_records} records inserted successfully."
    }
    ```

### Endpoints de Previsão

#### Recuperar Previsões

Busca uma lista de previsões armazenadas no banco de dados.

- Endpoint: `GET /predictions/`
- Parâmetros:
    - `skip (int, default=0)`: Número de registros a serem ignorados.
    - `limit (int, default=10)`: Número máximo de registros a serem retornados.
- Resposta:
    ```json
    {
    "message": "{num_records} records inserted successfully."
    }
    ```

#### Recuperar uma Previsão por ID

Busca uma previsão específica pelo seu ID.

- Endpoint: `GET /prediction_id/{ID}`
- Parâmetros:
    - `ID (str)`: O identificador único da previsão.
- Resposta:
    ```json
    {
    "ID": "1",
    "KNR": "4321",
    "Date": "1627852800",
    "Feature1": 42.0,
    "Feature2": 55.0,
    "Feature3": 62.0,
    "Prediction_result": 1,
    "Real_result": 1
    }
    ```
- Resposta de Erro:
    ```json
    {
    "detail": "Prediction not found"
    }
    ```

#### Atualizar uma Previsão

Atualiza as features e o resultado de previsão de uma previsão existente.

- Endpoint: `PUT /predictions/{ID}`
- Parâmetros:
    - `ID (str)`: O identificador único da previsão a ser atualizada.
- Resposta:
    ```json
    {
    "ID": "1",
    "KNR": "4321",
    "Date": "1627852800",
    "Feature1": 2.1,
    "Feature2": 1.234,
    "Feature3": 5.678,
    "Prediction_result": 1,
    "Real_result": 1
    }
    ```
- Resposta do Erro:
    ```json
    {
    "detail": "Prediction not found"
    }
    ```

#### Deletar uma Previsão

Deleta uma previsão específica pelo seu ID.

- Endpoint: `DELETE /predictions/{ID}`
- Parâmetros:
    - `ID (str)`: O identificador único da previsão a ser deletada.
- Resposta:
    ```json
    {
    "detail": "Prediction deleted"
    }
    ```

### Endpoints de Health Check

Healthcheck, ou verificação de saúde, é um processo utilizado para monitorar e garantir que os componentes de um sistema estejam funcionando corretamente. No contexto de uma aplicação web, um healthcheck é normalmente implementado como um endpoint que verifica a disponibilidade e a funcionalidade de diferentes partes do sistema, como o banco de dados, o modelo de machine learning, ou até mesmo o próprio servidor backend.

#### Health Check do Modelo

Este endpoint verifica se o modelo de machine learning está operacional. No código fornecido, ele realiza uma predição de teste para garantir que o modelo carregado está funcionando corretamente. Se o modelo consegue gerar uma predição, o status retornado é "ok".

- Endpoint: `GET /healthcheck/model`
- Resposta:
    ```json
    {
    "status": "ok",
    "prediction": 1.0
    }
    ```

#### Health Check do Banco de Dados

Este endpoint assegura que a conexão com o banco de dados está ativa e que o banco pode responder a consultas. Ele executa uma simples consulta SQL (SELECT 1) para confirmar a conexão. Se o banco de dados responde corretamente, o status retornado é "ok".

- Endpoint: `GET /healthcheck/db`
- Resposta:
    ```json
    {
    "status": "ok"
    }
    ```

#### Health Check do Backend

Este endpoint verifica se o servidor backend está em execução. Ele não realiza verificações adicionais além de confirmar que o backend consegue responder a uma requisição HTTP. O status retornado é "ok" se o servidor está ativo.

- Endpoint: `GET /healthcheck/backend`
- Resposta:
    ```json
    {
    "status": "ok"
    }
    ```

## Geração de UUIDv7

A aplicação utiliza uma função customizada de geração de UUIDv7 para criar identificadores únicos. O UUIDv7 é um UUID baseado em timestamp, fornecendo tanto exclusividade quanto ordenação temporal.

```python
def generate_uuidv7():
    timestamp_ms = int(time.time() * 1000)
    time_hex = f'{timestamp_ms:x}'
    random_hex = ''.join([f'{random.randint(0, 15):x}' for _ in range(26)])
    uuidv7 = f'{time_hex[:8]}-{time_hex[8:12]}-7{time_hex[12:15]}-{random_hex[:4]}-{random_hex[4:]}'
    return uuidv7
```

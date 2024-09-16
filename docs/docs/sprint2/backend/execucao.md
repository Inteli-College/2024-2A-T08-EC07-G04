---
title: Execução do Backend
slug: /execucao.md
---

# Execução do Backend

A aplicação foi desenvolvida utilizando o framework FastAPI, que permite a criação de APIs de forma rápida e eficiente. Para executar a aplicação, você precisa seguir os seguintes passos:

- Instalação das Dependências: Certifique-se de que todas as dependências estão instaladas. Você pode instalá-las utilizando o pip com o comando:

```bash
pip install fastapi sqlalchemy torch pandas psycopg2-binary
```

:::info
As dependências também podem ser instaladas através do requirements.txt, executando o comando `pip install -r requirements.txt`
:::

Este comando irá instalar as bibliotecas necessárias para rodar a aplicação, incluindo o FastAPI, SQLAlchemy, PyTorch, Pandas e o conector para o PostgreSQL.

- Configuração do Banco de Dados: Verifique se o banco de dados PostgreSQL está corretamente configurado e rodando. A string de conexão com o banco de dados deve estar configurada no código:

```python
DATABASE_URL = "postgresql://postgres:SENHA@localhost:5432/fillmore"
```

Substitua SENHA pela senha correta do usuário PostgreSQL.

- Criação do Banco de Dados: A aplicação criará automaticamente a tabela necessária no banco de dados na primeira execução, graças à configuração feita com SQLAlchemy. Não é necessário criar a tabela manualmente.

- Execução da Aplicação: Para iniciar o servidor da aplicação, utilize o comando abaixo no terminal:

```bash
uvicorn main:app --reload
```

    - `main` é o nome do arquivo Python que contém a aplicação FastAPI.
    - `app` é a instância da aplicação FastAPI.
    - A flag `--reload` é útil durante o desenvolvimento, pois recarrega automaticamente o servidor sempre que o código é alterado.

Após executar este comando, o servidor será iniciado e a aplicação estará disponível para receber requisições. Por padrão, o FastAPI serve a aplicação na URL http://127.0.0.1:8000.

- Interação com a API: Você pode acessar a documentação interativa da API gerada automaticamente pelo FastAPI no seguinte endereço:

```arduino
    http://127.0.0.1:8000/docs
```

Nesta página, você pode testar os endpoints da aplicação e visualizar as respostas diretamente no navegador.

- Monitoramento e Verificação: Após iniciar a aplicação, utilize os endpoints de healthcheck mencionados anteriormente para verificar se todos os componentes da aplicação estão funcionando corretamente.

Este processo garante que a aplicação esteja configurada corretamente, permitindo que você inicie o servidor e interaja com a API de maneira eficiente.
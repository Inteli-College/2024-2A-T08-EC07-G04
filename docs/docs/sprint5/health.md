# Alterações na HealthCheck

## Justificativa

A alteração na estrutura da HealthCheck foi feita para garantir o funcionamento das rotas, mesmo que o serviço do backend encontre problemas para rodar. Inicialmente, as rotas de healthcheck estavam dentro do backend, o que significava que, se o backend não estivesse rodando, o serviço de healthcheck também estaria indisponível. Com a alteração, o serviço de healthcheck torna-se independente do backend, garantindo que as rotas de healthcheck estejam sempre disponíveis, independentemente do status do backend.

## Estrutura do HealthCheck

```
/project-root 
│ ├── src 
│ ├── healthcheck 
│ │ ├── Dockerfile # Arquivo de configuração do Docker 
│ │ ├── healthcheck_service.py # Arquivo que lida com as requisições HTTP e rotas 
│ │ ├── requirements.txt # Dependências do projeto
```

## Rota `/healthcheck`

### Método: `GET`

### Descrição

A rota `/healthcheck` retorna o status de saúde de quatro componentes principais:

- **Backend**
- **Frontend**
- **Banco de Dados (PostgreSQL)**
- **PocketBase**

Ela faz chamadas assíncronas para cada um desses componentes e retorna um status indicando se o componente está **OK** ou **DOWN**.

### Exemplo de Resposta

```json
{
  "backend": "OK",
  "frontend": "OK",
  "database": "OK",
  "pocketbase": "OK"
}
```

### Estrutura da Resposta

- **backend**: O status de saúde do serviço de backend. Faz uma requisição HTTP para `http://backend:8000/` e verifica se a resposta foi um código 200.
  
- **frontend**: O status de saúde do serviço de frontend. Faz uma requisição HTTP para `http://frontend:4173/` e verifica se a resposta foi um código 200.
  
- **database**: O status de saúde do banco de dados PostgreSQL. Executa uma query `SELECT 1` para garantir que a conexão com o banco de dados está ativa.
  
- **pocketbase**: O status de saúde do serviço PocketBase. Faz uma requisição HTTP para `http://pocketbase:8090/_/` e verifica se a resposta foi um código 200.

## Detalhamento dos Métodos Auxiliares

1. **check_backend**: Faz uma requisição HTTP ao backend na URL `http://backend:8000/`. Retorna `OK` se a resposta for 200, caso contrário, retorna `DOWN`.
   
2. **check_frontend**: Faz uma requisição HTTP ao frontend na URL `http://frontend:4173/`. Retorna `OK` se a resposta for 200, caso contrário, retorna `DOWN`.

3. **check_database**: Conecta-se ao banco de dados PostgreSQL e executa a query `SELECT 1` para verificar a conectividade. Retorna `OK` se a query for bem-sucedida, ou `DOWN` caso contrário.

4. **check_pocketbase**: Faz uma requisição HTTP ao PocketBase na URL `http://pocketbase:8090/_/`. Retorna `OK` se a resposta for 200, caso contrário, retorna `DOWN`.

## Exceções e Tratamento de Erros

Cada método de verificação utiliza exceções para capturar erros de conectividade ou falhas no serviço. Se alguma requisição falhar (por exemplo, devido a timeout ou indisponibilidade do serviço), o status correspondente será marcado como **DOWN** e o erro será registrado no terminal para debug.

## Eventos de Inicialização e Encerramento

- **Startup**: Ao iniciar o aplicativo, um pool de conexões com o banco de dados PostgreSQL é criado.
  
- **Shutdown**: Quando o aplicativo é encerrado, o pool de conexões é fechado de maneira segura.
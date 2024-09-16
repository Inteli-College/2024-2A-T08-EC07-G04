---
title: Documentação das Rotas Implementadas no Backend
slug: /rotas.md
---
# Heath Check Controllers
O arquivo ```healthCheckController.py``` contém três funções principais que servem para verificar a saúde e o funcionamento correto de diferentes aspectos da aplicação backend.

:::info
## Utilização em Rotas
Para cada uma dessas funções, uma rota específica deve ser definida no módulo de routes, onde esses métodos de verificação de saúde serão associados a endpoints HTTP específicos. Geralmente, essas rotas podem ser acessadas por chamadas GET, permitindo uma integração fácil com sistemas de monitoramento que podem verificar periodicamente a saúde da aplicação.

Esse sistema de health check ajuda a identificar rapidamente problemas em ambientes de produção, facilitando a manutenção e a garantia da disponibilidade e confiabilidade do sistema. A documentação clara e detalhada dessas rotas também assegura que as operações de verificação possam ser compreendidas e utilizadas adequadamente tanto durante o desenvolvimento quanto em fases de operação e manutenção do sistema.
:::


1.```healthcheck_model()```
Esta função é responsável por verificar a saúde do modelo ou da lógica de negócios da aplicação. Ela tenta executar uma operação simples que, neste caso, é a atribuição de uma previsão simulada (test_prediction = 1.0). Se a operação for bem-sucedida, a função retorna um objeto JSON com o status "ok" e o valor da previsão. Em caso de falha, ela captura a exceção, retorna o status "error" e inclui a mensagem de erro no objeto JSON. Essa função é útil para garantir que a lógica de negócios da aplicação está funcionando conforme esperado.

2.```healthcheck_db(db: Session = Depends(get_db))```
Esta função verifica a saúde da conexão com o banco de dados. Utilizando a injeção de dependência fornecida pelo Depends(get_db), ela obtém uma sessão do banco de dados e executa uma consulta SQL básica (SELECT 1). Se a consulta for bem-sucedida sem exceções, a função retorna um objeto JSON com o status "ok". Caso contrário, ela captura a exceção, retorna o status "error" e a mensagem de erro correspondente. Esta função é crucial para assegurar que a aplicação pode se conectar e interagir com o banco de dados sem problemas.

3.```healthcheck_backend()```
A função healthcheck_backend() verifica a saúde geral do backend, sem depender de componentes externos como bancos de dados ou modelos de previsão. Simplesmente retorna um objeto JSON com o status "ok", indicando que o backend está operacional. Esta função pode ser utilizada para verificar rapidamente se o servidor backend está ativo e capaz de responder a solicitações.

# Prediction Controller
No arquivo ```predictionController.py```, diversas funções são definidas para gerenciar as previsões dos modelos, bem como operações básicas de CRUD (Create, Read, Update, Delete) relacionadas aos modelos, previsões e características envolvidas. A estrutura do código e as operações realizadas são detalhadas a seguir:

Inicialmente, o arquivo realiza a autenticação com um serviço ```PocketBase``` utilizando um email e senha pré-definidos. Se a autenticação for bem-sucedida, uma mensagem confirmando o sucesso é exibida; caso contrário, erros são capturados e detalhados, permitindo uma intervenção apropriada.

A ```função root()``` é um endpoint simples que retorna uma mensagem de boas-vindas, útil para verificar rapidamente se o serviço está ativo.

A ```função mock_data()``` permite a inserção de dados simulados no banco de dados para o modelo especificado. Isso é útil para testes e desenvolvimento, garantindo que o sistema pode manipular e reagir a diferentes volumes de dados.

O ```endpoint predict()``` é central para a aplicação, permitindo a previsão de resultados com base em dados carregados através de um arquivo. A função verifica se as colunas do arquivo estão corretas e utiliza o modelo carregado de uma URL específica para realizar previsões. Os resultados, juntamente com os dados de entrada, são armazenados no banco de dados, e um objeto JSON com o resultado da previsão é retornado.

As ```funções read_predictions()```, ```read_prediction()```, ```update_prediction()```, e ```delete_prediction()``` permitem a manipulação e consulta das previsões armazenadas no banco de dados, utilizando padrões comuns de operações CRUD. Estas funções garantem que os dados podem ser acessados, modificados e deletados de forma segura e eficiente.

Adicionalmente, a ```função update_model()``` permite atualizar as informações de um modelo no banco de dados, demonstrando a flexibilidade do sistema em adaptar-se a mudanças nas especificações ou atualizações dos modelos de previsão.

Em resumo, ```predictionController.py``` encapsula uma série de operações críticas para o funcionamento de uma aplicação de previsão baseada em modelos de inteligência artificial, com suporte robusto para autenticação, manipulação de dados, execução de previsões e manutenção de registros.
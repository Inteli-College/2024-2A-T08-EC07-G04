---
Title: backend da página de dashboard
sidebar-position: 1
---

# Dashboard Controller
O arquivo ```dashboardController.py``` todas as funções auxiliares e rotas necessárias para a geração dos gráficos e transmissão de informações para a página de dashboard.

:::info
## Utilização em Rotas
Para cada uma dessas funções, uma rota específica deve ser definida no módulo de routes no arquivo ```dashboardRoutes.py```, onde esses métodos serão associados a endpoints HTTP específicos. Geralmente, essas rotas podem ser acessadas por chamadas GET, permitindo uma integração fácil com sistemas de monitoramento que podem verificar periodicamente a saúde da aplicação.

Esse sistema funciona como uma camada de interação entre o backend e o frontend, processando os dados e transmitindo informações de maneira organizada para serem exibidas nos gráficos do dashboard. As funções descritas são usadas para buscar, processar e retornar estatísticas e métricas importantes, como contagens de previsões, KNRs únicos e registros de previsões semanais e diárias. Isso facilita o acompanhamento da saúde e desempenho do sistema ao longo do tempo, bem como a análise de tendências em falhas ou resultados das previsões.
:::


1.```normalize_to_current_month()```
Esta função retorna as datas de início e fim do mês atual. O primeiro dia é sempre o primeiro dia do mês, enquanto o último dia é o dia atual. Isso é utilizado para delimitar um período mensal atual para consultas relacionadas aos dados.

2.```get_last_5_months_ranges()```
Esta função retorna uma lista de dicionários com os intervalos de datas dos últimos cinco meses, começando do mês atual e retrocedendo até quatro meses anteriores. Cada dicionário contém as chaves `"start_date"` e `"end_date"`, representando o primeiro e último dia de cada mês. Esses intervalos são usados para calcular estatísticas mensais ao longo de múltiplos meses.

3.```count_unique_knr_and_prediction_result(db: Session, start_date: datetime, end_date: datetime) -> Dict[str, int]```
Esta função recebe uma sessão do banco de dados e um intervalo de datas, e retorna um dicionário contendo duas métricas:

- `"carros"`: a contagem de KNRs únicos no intervalo de datas especificado.
- `"falhas"`: a contagem de previsões cujo resultado (`prediction_result`) é igual a 1 no mesmo intervalo de tempo.

Essa função é útil para calcular a quantidade de carros monitorados e as falhas identificadas em um determinado período.

4.```get_timestamp_from_uuid(id_str: str) -> datetime```
Esta função converte uma string UUID em um objeto datetime, extraindo a parte correspondente ao timestamp do UUID. Ela é usada para obter a data de criação de um registro, dado que os IDs têm informações de timestamp incorporadas.

5.```read_predictions_current_week(skip: int, limit: int, db: Session = Depends(get_db)) -> List[dict]```
Esta função consulta todas as previsões na tabela `Prediction` e filtra as que foram criadas durante a semana atual, começando na segunda-feira. Ela aceita parâmetros `skip` e `limit` para paginação dos resultados. As previsões são retornadas como uma lista de dicionários, excluindo o estado da instância SQLAlchemy (`_sa_instance_state`). É utilizada para gerar dados para os gráficos de previsões feitas durante a semana corrente.

6.```read_predictions_current_day(skip: int, limit: int, db: Session = Depends(get_db)) -> List[dict]```
Esta função consulta todas as previsões na tabela `Prediction` e filtra as que foram criadas no dia atual. Semelhante à função anterior, ela utiliza `skip` e `limit` para paginação e retorna os registros em formato de lista de dicionários.
É usada para fornecer uma visão das previsões feitas no dia atual.

7.```get_unique_knr_predictions_last_5_months(db: Session = Depends(get_db)) -> Dict[str, Dict[str, int]]```
Esta função retorna um dicionário com as estatísticas dos últimos cinco meses. Para cada mês, são contados os KNRs únicos e as previsões com `prediction_result = 1`. Os resultados são armazenados em um dicionário, onde cada chave representa um mês (`"mes1"`, `"mes2"`, etc.), contendo sub-dicionários com as chaves `"carros"` e `"falhas"`.

Essa função é importante para analisar a evolução das métricas ao longo dos últimos cinco meses, possibilitando identificar tendências.

8.```count_unique_knr_last_month(db: Session = Depends(get_db)) -> int```
Esta função retorna a contagem de KNRs únicos no mês passado, com base no timestamp extraído do UUID de cada registro. Ela utiliza as datas de início e fim do mês atual para definir o intervalo de consulta.

Serve para monitorar quantos carros diferentes foram monitorados no mês anterior.

9.```count_predictions_last_month(db: Session = Depends(get_db)) -> int```
Esta função retorna a contagem de previsões com `prediction_result = 1` no mês passado, utilizando as datas de início e fim do mês atual como base para a consulta.

Essa métrica é usada para verificar quantas falhas foram previstas no último mês, ajudando a avaliar a qualidade e a precisão das previsões. 
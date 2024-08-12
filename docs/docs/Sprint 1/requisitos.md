# Requisitos de Viabilidade Técnica

## Objetivo da Proposta Geral do Sistema
O projeto, realizado em parceria com a Volkswagen, visa desenvolver um modelo preditivo e uma plataforma web para a visualização dos resultados. O modelo será treinado utilizando os dados fornecidos pela empresa, como resultados de testes, descrições de falhas e status de predições. A partir desses dados, o modelo terá a capacidade de prever possíveis falhas nos veículos, permitindo a potencial eliminação da etapa de rodagem, o que resultará em significativa redução de custos e benefícios ambientais.

A plataforma web que implementará o modelo incluirá funcionalidades para a inserção de novos dados, exibição imediata dos resultados das predições e uma interface para visualização dos dados coletados por meio de dashboards interativos.
## Descrição objetiva dos elementos gerais que vão compor a solução inicial proposta (diagrama de blocos)
Em relação aos componentes do sistema podemos destacar os dados de entrada, modelo preditivo e plataforma web. Por meio de uma descrição mais detalhada a respeito de cada elemento.<br/>
- **Dados de entrada**: É o conjunto de dados fornecidos pela empresa, incluindo resultados de testes, descrições de falhas e status das predições dos veículos. Os arquivos em questão estão maioria no formato Excel Spreadsheet(xlsx), e alguns em Comma-Separated Values(csv). Esses dados irão servir como base para o treinamento e funcionamento do modelo preditivo, pois alimentam o modelo com informações necessárias para identificar padrões e prever falhas. As tecnologias utilizadas para o desenvolvimento desse elemento serão para<br/>
- **Modelo Preditivo**: É o Algoritmo de machine learning treinado com os dados de entrada para prever possíveis falhas nos veículos e classificá-los de acordo com essas previsões. O modelo será capaz de processar os dados inseridos e gerar predições sobre a condição dos veículos. Ele é o ponto central da solução para a identificação de falhas e a orientação das inspeções.<br/>
- **Plataforma Web**: É a interface onde os usuários podem inserir novos dados de veículos para serem analisados pelo modelo preditivo. Essa plataforma terá, a principio, três telas principais, são elas: tela de inserção de dados, tela de exibição de resultados em tempo real e tela de dashboards interativos.<br/>
    - **Tela de Inserção de Dados**: Interface onde os usuários podem inserir novos dados de veículos para serem analisados pelo modelo preditivo.
    - **Tela Exibição dos Resultados em Tempo Real**: Interface que apresenta instantaneamente os resultados das predições realizadas pelo modelo, incluindo a classificação do veículo e as possíveis falhas.
    - **Tela de Dashboards Interativos**: Interface dedicada à visualização dos dados e métricas relacionadas ao desempenho do modelo, permitindo análises detalhadas e acompanhamento contínuo das predições e dos veículos analisados.





## Requisitos Funcionais
## Requisitos Não Funcionais
## Estudo da viabilidade Técnica
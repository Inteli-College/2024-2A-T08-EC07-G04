# Requisitos de Viabilidade Técnica
Aqui está a tabela com três colunas, conforme solicitado:

### Requisitos Funcionais

Os requisitos funcionais descrevem as funcionalidades essenciais que o sistema deve oferecer para atender às necessidades específicas do usuário e do negócio. Nesta seção, são detalhadas as capacidades que o sistema deve possuir, como a classificação preditiva de veículos, a interface de usuário, o treinamento contínuo do modelo, entre outras. Esses requisitos são fundamentais para garantir que o sistema desempenhe suas funções conforme esperado, proporcionando um ambiente eficiente e eficaz para a realização das inspeções de veículos.

| **Requisito** | **Nome** | **Descrição** |
|:---:|:---:|:---|
| **RF01** | Classificação Preditiva | - Classificar veículos em diferentes classes de inspeção com base em um modelo preditivo.<br />- Calcular a probabilidade de ocorrência de falhas e indicar o tipo de inspeção necessário para cada veículo. |
| **RF02** | Interface de Usuário | - Interface visual para o inspetor visualizar resultados do modelo preditivo e identificar o tipo de inspeção.<br />- Interface amigável e acessível para o analista de sistemas da fábrica. |
| **RF03** | Treinamento e Calibração do Modelo | - Receber novos dados de produção em tempo real para o treinamento do modelo.<br />- Permitir treinamento contínuo do modelo para manter ou melhorar a taxa de acerto. |
| **RF04** | Taxa de Acerto | - Objetivo de assertividade acima de 95%. |
| **RF05** | Entrada de Dados | - Receber dados da tabela `Predict.csv` com saída esperada na coluna `FALHAS_ROD` para o período de janeiro a abril de 2024. |
| **RF06** | Visualização e Relatórios | - Gerar relatórios sobre a probabilidade de falhas e o tipo de inspeção a ser realizada.<br />- Visualizar a classe predita e a probabilidade associada diretamente na interface. |
| **RF07** | Execução Local e em Cloud | - Funcionar em ambiente local com instruções claras para execução em nuvem.<br />- Demonstração em nuvem utilizando contas acadêmicas. |
| **RF08** | Limitações e Restrições | - Não incluir um processo longo de limpeza e adequação de dados.<br />- Não trabalhar com cenários de big data.<br />- Modelo não será disponibilizado fora do Google Colab. |

### Requisitos Não Funcionais

Os requisitos não funcionais definem as características de qualidade e as restrições que o sistema deve cumprir, além das funcionalidades básicas. Nesta seção, são abordados aspectos como desempenho, escalabilidade, usabilidade, confiabilidade, segurança, entre outros. Esses requisitos são essenciais para garantir que o sistema não apenas funcione corretamente, mas também atenda a padrões elevados de eficiência, segurança e facilidade de uso, assegurando uma experiência positiva para os usuários finais e a sustentabilidade da solução a longo prazo.

| **Requisito** | **Nome** | **Descrição** |
|:---:|:---:|:---|
| **RNF01** | Desempenho | - Processar dados e classificar veículos em tempo hábil, sem atrasos significativos.<br />- Resposta do modelo preditivo gerada em menos de 5 segundos. |
| **RNF02** | Escalabilidade | - Ser escalável para lidar com aumento de volume de dados, incluindo novas produções mensais, sem degradação de desempenho. |
| **RNF03** | Usabilidade | - Interface intuitiva e fácil de usar, com curva de aprendizado mínima.<br />- Layout claro, com instruções e resultados simples e acessíveis para usuários não técnicos. |
| **RNF04** | Confiabilidade | - Garantir alta disponibilidade, com tempo de inatividade mínimo.<br />- Garantir integridade dos dados durante entrada, processamento e saída. |
| **RNF05** | Manutenibilidade | - Fácil de manter e atualizar, especialmente em relação à recalibração e retraining do modelo preditivo.<br />- Código bem documentado para facilitar futuras modificações. |
| **RNF06** | Segurança | - Garantir segurança dos dados, com mecanismos contra acessos não autorizados.<br />- Controle de acesso adequado para diferentes usuários. |
| **RNF07** | Portabilidade | - Fácil de transportar entre diferentes ambientes (local e nuvem) sem grandes modificações.<br />- Usar tecnologias compatíveis com múltiplas plataformas. |
| **RNF08** | Compatibilidade | - Compatível com tecnologias existentes na fábrica da Volkswagen, especialmente na integração com outros sistemas de TI.<br />- Integração possível com sistemas de ERP ou outras bases de dados corporativas. |
| **RNF09** | Eficiência Energética | - Otimizado para uso eficiente de recursos computacionais, minimizando consumo de energia. |
| **RNF10** | Conformidade | - Conformidade com regulamentações e políticas de segurança de dados da Volkswagen do Brasil e normas de qualidade aplicáveis. |



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
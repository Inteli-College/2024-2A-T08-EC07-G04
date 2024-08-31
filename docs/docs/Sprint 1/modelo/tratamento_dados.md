---
title: Tratamento de dados
sidebar_position: 2
slug: /tratamento_dados
---

### **Tratamento inicial dos dados**

#### **Análise dos dados recebidos**

Foi recebido um volume significativo de arquivos Excel, sendo que cada um continha diversas tabelas. No entanto, considerando que algumas dessas tabelas já haviam sido utilizadas em um sistema existente da empresa, decidiu-se por não utilizar esses dados. Com essa filtragem, restaram duas categorias principais de arquivos: **resultados** e **falhas**. Cada categoria de arquivo apresentava a mesma estrutura de colunas e dados, sendo a categoria **resultados** apresentando dados de 2 meses de inspeções realizadas na linha de produção, enquanto os da categoria **falhas**, informações sobre os erros ocorridos na linha de produção, juntamente a identificação do modelo do veículo, quando, onde e quem relatou o problema.

#### **Concatenação de tabelas**

Como as tabelas de cada categoria tinham estruturas semelhantes, decidiu-se concatenar as que pertenciam à mesma categoria em uma única tabela, para facilitar a análise e o tratamento dos dados. Para isso, foi utilizada a biblioteca Pandas, do Python, que permitiu analisar cada arquivo Excel, identificar as tabelas e, em seguida, unificar os dados de acordo com suas categorias em uma tabela consolidada para cada categoria.

#### **Ajuste de colunas**

Ao analisar cada uma das tabelas unificadas, foi observado que alguns dados não eram relevantes para o problema apresentado pelo cliente. O projeto deve focar apenas na construção de um modelo para um carro específico. Além disso, informações como a pessoa que reportou a falha não são relevantes para a criação e o treinamento do nosso modelo. Portanto, foram feitos ajustes na tabela de **falhas**, removendo todos os dados relacionados a outros modelos de carro e excluindo a coluna que indicava quem reportou a falha.

Além disso, o projeto deve prever ocorrências em uma estação específica da fábrica. Com isso em mente, e considerando o tamanho das tabelas, inicialmente optou-se por filtrar os dados apenas dessa estação e remover aqueles que se referiam a outras.

Esses ajustes reduziram significativamente a quantidade de dados, tornando-a mais manejável e adequada para criar um modelo sem demandar alta capacidade computacional. Decidiu-se trabalhar com menos dados em um primeiro momento, pois o objetivo inicial é testar o tratamento, a análise e a seleção de features para a construção do primeiro modelo.

#### **Mescla das tableas**

Para criar o modelo de inteligência artificial (IA), foi necessário combinar a tabela de **resultados** com a tabela de **falhas**. Como essas tabelas tinham estruturas diferentes, não foi possível simplesmente concatená-las. Em vez disso, foi realizado um _merge_ com base no identificador de cada carro, o que permitiu adicionar as colunas de ambas as tabelas em uma única tabela, utilizando o identificador como o elo de união.

Entretanto, surgiram casos em que um identificador estava presente em uma tabela, mas não na outra. Esse problema foi tratado de duas maneiras: se o identificador estava na tabela **falhas**, mas ausente na tabela **resultados**, a linha correspondente foi excluída, pois a falta de resultados de testes para aquela falha poderia comprometer a precisão do modelo. Por outro lado, quando o identificador estava na tabela **resultados**, mas ausente na tabela **falhas**, o dado foi mantido. Isso permite que o modelo reconheça situações em que o carro não apresenta falhas, ajudando na análise sobre a presença ou ausência de problemas.

#### **Separação da coluna ID**

A coluna de ID representa o tipo de inspeção realizada no carro. Como há apenas três tipos de inspeção, essa coluna foi dividida em três colunas separadas, cada uma correspondente a um tipo de ID. Dessa forma, o modelo consegue distinguir melhor as inspeções e os tipos de falhas, o que aumenta a precisão na previsão da área e do tipo de falha apresentada.

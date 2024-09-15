---
title: Documentação do Datalake
slug: /datalake.md
---

# O que é um Data Lake?

Um **Data Lake** é um repositório centralizado que permite armazenar uma grande quantidade de dados em sua forma bruta, sejam eles estruturados, semiestruturados ou não estruturados. Diferente de um Data Warehouse, que requer que os dados sejam limpos, transformados e organizados antes de serem armazenados, o Data Lake armazena os dados em seu estado original, sem a necessidade de um esquema predefinido. Essa flexibilidade é uma de suas principais características, permitindo que dados de diversas fontes, como bancos de dados, logs de aplicativos, sensores IoT, redes sociais, entre outros, sejam armazenados de maneira simples e escalável.

# Como Funciona um Data Lake?

O funcionamento de um Data Lake envolve a ingestão de dados de diferentes fontes, que podem ser carregados em tempo real ou em lotes. Esses dados são armazenados em sua forma original e podem ser processados posteriormente com o uso de ferramentas de Big Data, como Apache Spark e Hadoop, que facilitam a realização de análises desde relatórios simples até modelos avançados de aprendizado de máquina. Apesar de armazenar dados em sua forma bruta, um Data Lake também oferece mecanismos de governança para garantir a segurança, qualidade e conformidade dos dados, utilizando controles de acesso e monitoramento rigorosos.

# Por Que Não Utilizar um Data Lake no Projeto com a Volkswagen?

No entanto, um Data Lake pode não ser a melhor opção para todos os tipos de projetos, especialmente para o projeto que estamos desenvolvendo para a Volkswagen. O projeto visa criar um modelo preditivo para classificar veículos quanto às possíveis falhas que podem ocorrer durante o processo de inspeção de rodagem. Nesse contexto, optar por um Data Lake apresentaria algumas desvantagens.

Em primeiro lugar, a implementação e manutenção de um Data Lake introduziriam uma complexidade significativa. A infraestrutura necessária para um Data Lake envolve não apenas o armazenamento de dados, mas também a configuração de pipelines de ingestão, governança de dados, segurança, e uma equipe especializada para gerenciar tudo isso. Para o nosso projeto, que é relativamente focado e possui um escopo bem definido, essa complexidade seria um excesso desnecessário.

# A Natureza dos Dados e a Eficiência do Projeto

Além disso, o projeto da Volkswagen envolve a manipulação de um conjunto de dados relativamente estruturado e específico, como dados de sensores e logs de testes de veículos. Utilizar um Data Lake, que é ideal para ambientes com grandes volumes de dados diversos e heterogêneos, não traria os benefícios esperados. Em vez disso, um banco de dados relacional ou um Data Warehouse, que oferece acesso rápido e eficiente a dados organizados, seria mais adequado para as necessidades específicas de nosso modelo preditivo.

# Desempenho e Custo

Outro ponto a considerar é a latência e o tempo de resposta. A arquitetura de um Data Lake pode resultar em maior latência para consultas específicas e análises interativas, o que não é ideal para o ambiente de inspeção de rodagem da Volkswagen, onde a agilidade na tomada de decisões é crucial. No nosso caso, soluções mais otimizadas e direcionadas, como bancos de dados que suportam consultas rápidas, podem fornecer um desempenho mais adequado.

Por fim, o custo e a manutenção de um Data Lake podem ser significativos. Para o nosso projeto, onde os recursos precisam ser utilizados de maneira eficiente, a adoção de um Data Lake poderia significar um gasto desnecessário com infraestrutura e pessoal. Nosso foco é desenvolver um modelo preditivo eficaz dentro das limitações de tempo e orçamento, e uma solução mais simples e direta é suficiente para alcançar os objetivos definidos.

# Conclusão

Portanto, ao considerar o escopo, os objetivos e os requisitos específicos do projeto com a Volkswagen, a escolha de não utilizar um Data Lake se baseia na busca por uma solução que seja mais eficiente, menos complexa, mais rápida e de menor custo, garantindo que o modelo preditivo seja implementado de forma eficaz e atenda às expectativas da empresa.

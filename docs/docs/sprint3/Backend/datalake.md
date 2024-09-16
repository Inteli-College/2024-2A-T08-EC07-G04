---
title: Documentação do Datalake
slug: /datalake.md
---

# O que é um Data Lake?

Um **Data Lake** é um repositório centralizado que permite armazenar uma grande quantidade de dados em sua forma bruta, sejam eles estruturados, semiestruturados ou não estruturados. Diferente de um Data Warehouse, que requer que os dados sejam limpos, transformados e organizados antes de serem armazenados, o Data Lake armazena os dados em seu estado original, sem a necessidade de um esquema predefinido. Essa flexibilidade é uma de suas principais características, permitindo que dados de diversas fontes, como bancos de dados, logs de aplicativos, sensores IoT, redes sociais, entre outros, sejam armazenados de maneira simples e escalável.

# Como Funciona um Data Lake?

O funcionamento de um Data Lake envolve a ingestão de dados de diferentes fontes, que podem ser carregados em tempo real ou em lotes. Esses dados são armazenados em sua forma original e podem ser processados posteriormente com o uso de ferramentas de Big Data, como Apache Spark e Hadoop, que facilitam a realização de análises desde relatórios simples até modelos avançados de aprendizado de máquina. Apesar de armazenar dados em sua forma bruta, um Data Lake também oferece mecanismos de governança para garantir a segurança, qualidade e conformidade dos dados, utilizando controles de acesso e monitoramento rigorosos.

# Por Que Não Utilizar um Data Lake no Projeto com a Volkswagen?

No entanto, um Data Lake pode não ser a melhor opção para todos os tipos de projetos, pois seus benefícios podem ser extraídos de outra forma no projeto, dependendo da arquitetura. Os maiores benefícios de um Data Lake seriam a possibilidade de quartar altas quantidades de informação, de qualquer forma (estruturada, semi-estruturada e não estruturada) e conseguir tratar os dados dentro do datalake. 

Porém, no nosso projeto, como os dados são fornecidos pela Volkswagen e não recebemos os dados brutos coletados, eles já apresentam um tratamento inicial de dados. Sendo assim, todas as informações conseguem ser guardadas por um banco de dados relacional, que apresenta dados estruturados. Pela arquitetura criada do banco de dados, consegue-se armazenar todos os dados que serão utilizados no projeto, assim não havia necessidade de aumentar a complexidade do projeto para esse ponto.

Quanto ao armazenamento de modelos, que podem ser considerados dados semi-estruturados ou não estruturados, optou-se por utilizar o `Pocketbase`. O `Pocketbase` é uma ferramenta leve e versátil que permite o armazenamento e gerenciamento de dados através de uma interface simples e eficiente. Neste projeto, ele está sendo utilizado exclusivamente para armazenar os modelos de machine learning. A principal vantagem é que o `Pocketbase` gera URLs para cada modelo armazenado, facilitando o carregamento e a utilização desses modelos na aplicação. Assim, podemos acessar e utilizar os modelos diretamente a partir dos URLs gerados pelo `Pocketbase`, integrando-os de forma eficiente ao fluxo de trabalho do projeto.  

# A Natureza dos Dados e a Eficiência do Projeto

Além disso, o projeto da Volkswagen envolve a manipulação de um conjunto de dados relativamente estruturado e específico, como dados de sensores e logs de testes de veículos. Utilizar um Data Lake, que é ideal para ambientes com grandes volumes de dados diversos e heterogêneos, não traria os benefícios esperados. Em vez disso, um banco de dados relacional ou um Data Warehouse, que oferece acesso rápido e eficiente a dados organizados, seria mais adequado para as necessidades específicas de nosso modelo preditivo.

# Desempenho e Custo

Outro ponto a considerar é a latência e o tempo de resposta. A arquitetura de um Data Lake pode resultar em maior latência para consultas específicas e análises interativas, o que não é ideal para o ambiente de inspeção de rodagem da Volkswagen, onde a agilidade na tomada de decisões é crucial. No nosso caso, soluções mais otimizadas e direcionadas, como bancos de dados que suportam consultas rápidas, podem fornecer um desempenho mais adequado.

Por fim, o custo e a manutenção de um Data Lake podem ser significativos. Para o nosso projeto, onde os recursos precisam ser utilizados de maneira eficiente, a adoção de um Data Lake poderia significar um gasto desnecessário com infraestrutura e pessoal. Nosso foco é desenvolver um modelo preditivo eficaz dentro das limitações de tempo e orçamento, e uma solução mais simples e direta é suficiente para alcançar os objetivos definidos.

# Conclusão

Portanto, ao considerar o escopo, os objetivos e os requisitos específicos do projeto com a Volkswagen, a escolha de não utilizar um Data Lake se baseia na busca por uma solução que seja mais eficiente, menos complexa, mais rápida e de menor custo, garantindo que o modelo preditivo seja implementado de forma eficaz e atenda às expectativas da empresa.

## Análise Financeira

### Introdução:
&emsp;&emsp;Nessa seção, abordaremos a análise financeira da prova de conceito e da implementação do projeto final, observando todos os custos a serem considerados, desde o desenvolvimento até a manutenção do servidor em nuvem.  
&emsp;&emsp;O projeto visa desenvolver um modelo preditivo capaz de identificar possíveis falhas no processo de montagem de carros nas fábricas da Volkswagen, evitando que esses carros sejam enviados para as concessionárias com defeito de fabricação.

### Proof of Concept (PoC)
&emsp;&emsp;A PoC, do inglês "Proof of Concept" (prova de conceito), é o experimento realizado previamente ao projeto final, com a finalidade de provar sua viabilidade. Pensando nisso, fizemos a análise financeira da implementação dessa prova de conceito, levando em conta os custos de hardware, que dizem respeito aos computadores utilizados no desenvolvimento, a mão de obra e o custo de manutenção em nuvem. Segue abaixo uma tabela com a análise completa:

<p align="center">

| Descrição                                      | Quantidade | Custo Unitário | Valor Final   | Fonte |
| ---------------------------------------------- | ---------- | -------------- | ------------- | ------------------- |
| Hardware (computadores) | 3 | R$4.422,00 | R$13.266,00 | [Dell](https://www.dell.com/pt-br/shop/cty/pdp/spd/latitude-14-3440-laptop/ctol3440adl_p12h?redirectTo=SOC&tfcid=31768715&gacd=9657105-15015-5761040-275878141-0&dgc=ST&cid=71700000114503108&gad_source=1&gclid=Cj0KCQjw5ea1BhC6ARIsAEOG5pyFb_VRapQS8Ic_a-Cwq6DBVRaJ06WdP6QxzHP1y8CQvy-fPgNnFr4aAnq5EALw_wcB&gclsrc=aw.ds) |
| Engenheiros de Dados (Por 2 meses) | 2 | R$18.000,00 | R$36.000,00 | [Glassdoor](https://www.glassdoor.com.br/Salários/engenheiro-de-dados-salário-SRCH_KO0,19.htm#:~:text=A%20remuneração%20total%20mensal%20estimada,salários%20coletados%20de%20nossos%20usuários.) |
| Gestor de Projetos (Por 2 meses) | 1 | R$26.770,00 | R$26.770,00 | [Glassdoor](https://www.glassdoor.com.br/Salários/gerente-de-projetos-de-ti-salário-SRCH_KO0,25.htm#:~:text=A%20média%20salarial%20do%20cargo,%24%20805%20e%20R%24%203.508.) |
| Total de Mão de Obra | | | R$62.770,00 | |
| **Total Geral** |   |   | **R$76.036,00** | |
| Margem de lucro | 20% | | R$15.207,00 | |
| Subtotal | | | R$91.243,00 | |
| Imposto |  18% | | R$13.918,00 |  |
| **Preço Mínimo Aceitável** | | | **R$118.428,00** | |

</p>

&emsp;&emsp;Seguindo a análise acima, é possível observar o preço mínimo aceitável para o desenvolvimento da PoC, contemplando todos os gastos de material e mão de obra, aplicando uma margem de lucro válida e cumprindo todas as obrigações fiscais. Abaixo, observa-se a análise dos custos de manutenção desta PoC em nuvem.

<p align="center">

| Serviço: | Quantidade | Valor/Mês: | Total: |
| --- | --- | --- | --- |
| Armazenamento | 256 GB | R$0,13 por GB | R$33,28 |
| ETL | 25 horas | R$2,41 por DPU-Hora | R$60,28 |
| Treinamento | 12 horas e meia | R$4,93 por hora | R$61,63 |
| Monitoramento | 256 GB | R$1,64 por GB | R$420,86 |
| Catalogação | 25 mil itens | R$0,55 a cada mil itens | R$13,70 |
| **Total Final** | | | **R$589,75** |

</p>

&emsp;&emsp;Foi possível chegar a essa precificação com base no site [AWS Pricing Calculator](https://calculator.aws/#/) e permite ter uma noção do custo mensal da manutenção do serviço na nuvem.

### Projeto final
&emsp;&emsp;Na análise financeira do projeto final, foram considerados custos ampliados, uma vez que a implementação demandará maior quantidade de recursos em termos de hardware, software, mão de obra, e custos de manutenção mais elevados. Abaixo, a tabela completa com os custos do projeto final:

<p align="center">

| Descrição                                      | Quantidade | Custo Unitário | Valor Final   | Fonte |
| ---------------------------------------------- | ---------- | -------------- | ------------- | ------------------- |
| Hardware (computadores) | 6 | R$7.061,00 | R$42.366,00 | [Dell](https://www.dell.com/pt-br/shop/cty/pdp/spd/latitude-14-5450-laptop/cto01l5450bcc_p21?redirectTo=SOC&tfcid=31768715&gacd=9657105-15015-5761040-275878141-0&dgc=ST&cid=71700000114503108&gad_source=4&gclid=Cj0KCQjwiOy1BhDCARIsADGvQnBBiTftEtWcLGdI1hQbztwUDsmY606ieK9kg6cxyecXnQTJj5w7XNAaAneeEALw_wcB&gclsrc=aw.ds) | 
| Licenças de Software | 1 | R$300,00 | R$300,00 | |
| Desenvolvimento Customizado (100 horas) | 100 | R$50,00 | R$5.000,00 | |
| Engenheiros de Dados (Por 2 meses) | 3 | R$18.000,00 | R$54.000,00 | [Glassdoor](https://www.glassdoor.com.br/Salários/engenheiro-de-dados-salário-SRCH_KO0,19.htm#:~:text=A%20remuneração%20total%20mensal%20estimada,salários%20coletados%20de%20nossos%20usuários.) |
| Engenheiro de Software (Por 2 meses) | 2 | R$16.000,00 | R$32.000,00 | [Glassdoor](https://www.glassdoor.com.br/Salários/engenheiro-de-software-salário-SRCH_KO0,22.htm) |
| Gestor de Projetos (Por 2 meses) | 1 | R$26.770,00 | R$26.770,00 | [Glassdoor](https://www.glassdoor.com.br/Salários/gerente-de-projetos-de-ti-salário-SRCH_KO0,25.htm#:~:text=A%20média%20salarial%20do%20cargo,%24%20805%20e%20R%24%203.508.) |
| Total de Software | | | R$5.300,00 |  |
| Total de Mão de Obra | | | R$112.770,00 | |
| **Total Geral** |   |   | **R$160.436,00** | |
| Margem de lucro | 20% | | R$32.087,00 | |
| Subtotal | | | R$192.523,00 | |
| Imposto |  18% | | R$29.368,00 |  |
| **Preço Mínimo Aceitável** | | | **R$221.891,00** | |

</p>

&emsp;&emsp;A tabela acima reflete o preço mínimo aceitável para o desenvolvimento do projeto final, considerando todos os custos envolvidos e as devidas margens de lucro e impostos. A seguir, apresentamos os custos de manutenção do projeto em nuvem, que foram ampliados em relação à PoC devido ao maior volume de dados e processos.

<p align="center">

| Serviço: | Quantidade | Valor/Mês: | Total: |
| --- | --- | --- | --- |
| Armazenamento | 1024 GB | R$0,13 por GB | R$133,12 |
| ETL | 100 horas | R$2,41 por DPU-Hora | R$241,12 |
| Treinamento | 50 horas | R$4,93 por hora | R$246,50 |
| Monitoramento | 1024 GB | R$1,64 por GB | R$1.683,46 |
| Catalogação | 100 mil itens | R$0,55 a cada mil itens | R$55,00 |
| **Total Final** | | | **R$2.359,20** |

</p>

&emsp;&emsp;Assim como a precificação da PoC, a tabela acima também foi feita utilizando o [AWS Pricing Calculator](https://calculator.aws/#/), porém com proporções muito maiores, visto que é referente a implementação final do projeto.
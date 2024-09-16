---
title: Análise dos dados
sidebar_position: 3
slug: /analise_dados
---

### **Análise dos Dados e Criação de Features**

#### **Análise Inicial dos Dados:**

O primeiro passo fundamental no projeto foi a realização de uma **Análise Exploratória dos Dados**. Essa etapa inicial é essencial para compreender a estrutura e as peculiaridades do dataset, permitindo a identificação de padrões e possíveis anomalias que possam impactar a modelagem posterior. Os dados que foram analisados abrangiam uma ampla gama de medições e estados relacionados a componentes identificados nos tipos de grupo de operações: `ID1`(Operação máquinas), `ID2`(Operação parafusos) e `ID718`(Operação eletrônica). Esses componentes representam diferentes partes de um sistema operacional cuja performance e falhas precisavam ser monitoradas e previstas.

Durante a análise, foram avaliadas as características estatísticas básicas, como média, mediana, desvio padrão e distribuição das variáveis. Essa abordagem permitiu uma compreensão mais profunda do comportamento dos dados, especialmente em termos de variabilidade e distribuição das diferentes medições. Além disso, foi fundamental verificar a presença de **outliers** e **valores ausentes** que pudessem distorcer as análises subsequentes. Identificamos que certos valores estavam fora das faixas esperadas, indicando possíveis erros de medição ou eventos raros que poderiam influenciar os resultados.

#### **Tratamento de Dados Ausentes:**

Um dos desafios identificados durante a análise foi a presença de **valores ausentes** ou **NaN** em várias colunas, particularmente nas relacionadas aos status OK(10) e NOK(13). Interpretamos a ausência de dados como a não ocorrência de um evento (ou seja, a ausência de um estado OK ou NOK foi considerada equivalente a 0). Com isso em mente, foi adotada a estratégia de **substituir os valores ausentes por zeros**. Essa decisão foi baseada na suposição de que, na ausência de um registro explícito, o componente não apresentou nenhum comportamento fora do normal que precisasse ser marcado.

#### **Conversão de Tipos:**

Durante a preparação dos dados, outra questão que precisou ser abordada foi a conversão de tipos de dados. Algumas colunas, que originalmente continham informações numéricas, estavam armazenadas como strings (texto). Isso pode ocorrer quando os dados são importados de fontes heterogêneas ou quando há problemas na formatação dos arquivos de origem. Para permitir que essas colunas fossem incluídas em análises estatísticas e no processo de criação de novas features, foi necessário converter essas variáveis de strings para um formato **numérico**. Essa conversão foi realizada usando a função `pd.to_numeric`, que converte strings em números inteiros ou decimais, tratando qualquer erro de conversão como valores faltantes, que foram subsequentemente tratados.

#### **Criação de Features:**

Com os dados limpos e padronizados, a próxima etapa foi a criação de novas **features** que pudessem capturar de maneira mais eficaz a relação entre os diferentes componentes e seus estados. A criação de features é uma prática essencial na preparação de dados para modelos de machine learning, pois permite sintetizar informações complexas em variáveis mais simples e interpretáveis, além de ser uma melhor prática para que posteriormente o modelo possa ser treinado.

As features do primeiro modelo:

- **KNR**: Identificação, feature já existente anteriormente

- **ID1 QT, ID2 QT, ID718 QT:** Quantidade de cada operação realizada no KNR.

- **ID1 S NOK, ID2 S NOK, ID718 S NOK:** De maneira semelhante, essas features capturam o número de vezes que os componentes ID1, ID2, e ID718 estiveram em estado NOK (valor 13), conforme identificado pelo modelo. Essas contagens são fundamentais para entender a propensão de cada componente a falhar e ajudam na análise do comportamento do sistema em condições adversas.

- **ID1 S OK, ID2 S OK, ID718 S OK:** Essas features representam o número de vezes que os componentes ID1, ID2, e ID718 estiveram no estado OK (valor 10), conforme determinado pelo modelo. Cada feature contabiliza as ocorrências do estado 10 para o respectivo componente, fornecendo uma visão detalhada da frequência de funcionamento correto.

- **TOTAL OK:** Essa feature foi criada somando os estados OK para cada um dos componentes `ID1`, `ID2`, e `ID718`. Ela serve como um indicador geral de bom funcionamento do sistema. Uma alta contagem de OKs sugere que os componentes estão operando dentro dos parâmetros esperados.
  
- **TOTAL NOK:** Similar ao `TOTAL OK`, esta feature soma os estados NOK para os componentes. Ela é essencial para identificar quantas vezes os componentes falharam ou apresentaram problemas, o que é crucial para prever e entender os padrões de falha.
  
- **RESULTADO:** Para simplificar a classificação, foi criada uma variável binária chamada `RESULTADO`. Esta variável assume o valor de 1 quando todos os componentes estão em estado OK, indicando que o sistema está operando sem falhas. Caso contrário, se pelo menos um componente apresentar um estado NOK, a variável assume o valor de 0, sinalizando a ocorrência de uma falha em alguma parte do sistema.

- **FALHA_OPER:** Esta feature categórica foi desenvolvida para identificar qual operação específico falhou, caso tenha ocorrido uma falha. Ela é derivada das colunas de estados NOK, mapeando o componente que apresentou a falha. Se nenhum componente apresentou falha, essa variável assume o valor `Nenhuma`, indicando que o sistema está operando normalmente.

Essas features foram desenhadas para capturar as dinâmicas essenciais dos dados, permitindo que os modelos possam interpretar e aprender padrões relevantes de maneira mais eficaz. Além disso, elas ajudam a reduzir a complexidade do dataset, concentrando a informação crítica em variáveis específicas e mais fáceis de manejar durante a fase de modelagem.


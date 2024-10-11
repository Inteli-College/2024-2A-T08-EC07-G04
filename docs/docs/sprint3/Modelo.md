# Evolução do Modelo

Nesta sprint, o foco principal foi melhorar o desempenho de um modelo de classificação binária utilizado para prever falhas. O modelo original apresentava uma boa acurácia, porém, percebemos que havia espaço para ajustes e melhorias. Durante o processo, aplicamos diversas técnicas para otimizar a capacidade do modelo de generalizar melhor para novos dados, além de buscar uma maneira mais robusta de avaliar seu desempenho em diferentes métricas.

## Situação Inicial

O modelo original era uma rede neural simples, composta por duas camadas densas. A configuração inicial consistia em uma primeira camada com 16 neurônios, seguida por uma camada com 8 neurônios, ambas utilizando a função de ativação `ReLU`. A última camada utilizava a função de ativação `sigmoid`, para que o modelo pudesse realizar uma classificação binária (falha ou não falha):

```python
model = Sequential([
    Dense(16, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])
```

A acurácia inicial do modelo no conjunto de teste estava em torno de 94.32%. Embora o resultado fosse considerado bom, percebemos que poderíamos melhorar, especialmente em relação ao comportamento do modelo em classes desbalanceadas e no controle de overfitting.

## Implementação de Novas Features

Nosso primeiro passo foi retornar aos dados em busca de formas de utilizá-los de forma mais abrangente. O resultado dessa busca foi a adição de novas features ao modelo, passando a tratar colunas como VALUE_ID, VALUE e UNIT. Como resultado as features do modelo foram definidas como:

['unique_names', '1_status_10', '2_status_10', '718_status_10', '1_status_13', '2_status_13', '718_status_13',
            '_unit_count', '%_unit_count', 'Clicks_unit_count', 'Deg_unit_count', 'Grad_unit_count', 'Nm_unit_count',
            'Unnamed:5_unit_count', 'V_unit_count', 'kg_unit_count', 'min_unit_count', 'mm_unit_count', '_unit_mean',
            '%_unit_mean', 'Clicks_unit_mean', 'Deg_unit_mean', 'Grad_unit_mean', 'Nm_unit_mean', 'Unnamed:5_unit_mean',
            'V_unit_mean', 'kg_unit_mean', 'min_unit_mean', 'mm_unit_mean']



## Técnicas Utilizadas para Melhorar o Modelo

Nesta sprint, várias abordagens foram implementadas para otimizar o desempenho do modelo. Começamos ajustando os hiperparâmetros por meio do uso de **Random Search**. Essa técnica nos permitiu testar diferentes combinações de parâmetros, como o número de épocas (epochs), o tamanho do batch e o otimizador utilizado. Aqui está o código usado para a pesquisa de hiperparâmetros:

```python
from sklearn.model_selection import RandomizedSearchCV
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier

# Função para construir o modelo
def build_model(optimizer='adam'):
    model = Sequential([
        Dense(16, activation='relu', input_shape=(X_train_scaled.shape[1],)),
        Dense(8, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Usando RandomizedSearchCV
param_grid = {'batch_size': [16, 32, 64], 'epochs': [100, 200, 300], 'optimizer': ['adam', 'rmsprop']}
model = KerasClassifier(build_fn=build_model)
random_search = RandomizedSearchCV(estimator=model, param_distributions=param_grid, n_iter=5, cv=3, verbose=1)
random_search.fit(X_train_scaled, y_train_balanced)
```

Os melhores hiperparâmetros encontrados foram 100 épocas, batch size de 64 e o otimizador RMSprop. Isso resultou em uma acurácia revisada de 96.76%, com uma redução no tempo de treinamento, tornando o processo mais eficiente.

Além dos ajustes nos hiperparâmetros, também introduzimos técnicas para evitar que o modelo se sobreajustasse aos dados de treinamento. Para isso, adicionamos camadas de **Dropout** e **Regularização L2**:

```python
from tensorflow.keras.regularizers import l2

model = Sequential([
    Dense(32, activation='relu', input_shape=(X_train_scaled.shape[1],), kernel_regularizer=l2(0.001)),
    Dropout(0.3),  # Dropout de 30% para reduzir overfitting
    Dense(16, activation='relu', kernel_regularizer=l2(0.001)),
    Dropout(0.3),  # Outro Dropout
    Dense(1, activation='sigmoid')
])
```

O Dropout é uma técnica que desativa aleatoriamente neurônios durante o treinamento, evitando que o modelo dependa demais de combinações específicas de neurônios. Já a regularização L2 adiciona uma penalidade ao erro do modelo quando os pesos ficam muito grandes, ajudando a controlar o overfitting. Com essas adições, conseguimos criar um modelo mais robusto, que não apenas manteve uma acurácia alta (93.55%), mas também mostrou um comportamento mais estável entre os conjuntos de treinamento e validação, evidenciando uma generalização melhor para dados novos.

Outra técnica importante que aplicamos foi o uso de SMOTE (Synthetic Minority Over-sampling Technique). O SMOTE é usado para balancear as classes no conjunto de treinamento, criando novas amostras sintéticas para a classe minoritária (neste caso, as falhas):

```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

```

Isso nos ajudou a melhorar a sensibilidade e o recall do modelo, garantindo que ele não ignorasse a classe de falhas, que era menos frequente nos dados.

## Avaliação do Desempenho

Após implementar essas melhorias, focamos em realizar uma análise mais aprofundada do desempenho do modelo. Adicionamos a **Curva ROC (Receiver Operating Characteristic)** à avaliação para medir a qualidade das previsões probabilísticas:

```python
from sklearn.metrics import roc_curve, auc

# Previsões do modelo
y_pred_proba = model.predict(X_test_scaled)

# Calcular a curva ROC
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

# Plot da curva ROC
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()
```

## Considerações Finais
No geral, os ajustes realizados durante essa sprint no modelo trouxeram várias melhorias importantes. Por meio da introdução de novas features e dmais mudanças obtivemos uma melhoria significativa no nosso modelo, mas, mais importante, criamos um modelo mais robusto e menos suscetível a overfitting. O uso de técnicas como Dropout e Regularização L2, além do balanceamento das classes com SMOTE, proporcionaram uma solução que se comporta de maneira mais estável em diferentes cenários.

Apesar de termos avançado bastante, ainda há áreas que podem ser exploradas, especialmente no que diz respeito à Curva ROC, cuja AUC foi de 0.67. Isso sugere que podemos continuar refinando a seleção de features e ajustar o threshold de classificação para otimizar o desempenho.
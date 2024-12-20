# Importação das bibliotecas necessárias
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns

# ---- 1. Carregando o Dataset ----
# Baixar manualmente o dataset em https://www.kaggle.com/prathums/heart-disease-prediction
# Atualize o caminho conforme o local onde você salvou o arquivo.
df = pd.read_csv("heart.csv")

# ---- 2. Breve Visualização dos Dados ----
print("Visualização inicial dos dados:")
print(df.head())
print("\nInformações gerais:")
print(df.info())

# ---- 3. Pré-processamento ----
# Separando as variáveis preditoras (X) e a variável alvo (y)
X = df.drop(columns=['target'])
y = df['target']

# Padronizando os dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividindo o dataset em treino e teste (70% treino, 30% teste)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# ---- 4. Treinamento do Modelo ----
# Utilizando um Classificador de Rede Neural
mlp = MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=1000, random_state=42)
mlp.fit(X_train, y_train)

# ---- 5. Avaliação do Modelo ----
# Previsões
y_pred = mlp.predict(X_test)
y_pred_prob = mlp.predict_proba(X_test)[:, 1]

# Relatório de classificação
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

# Matriz de Confusão
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['No Disease', 'Disease'], yticklabels=['No Disease', 'Disease'])
plt.title('Matriz de Confusão')
plt.xlabel('Previsão')
plt.ylabel('Real')
plt.show()

# Curva ROC
fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
roc_auc = roc_auc_score(y_test, y_pred_prob)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.2f}')
plt.plot([0, 1], [0, 1], 'k--')
plt.title('Curva ROC')
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.legend(loc='lower right')
plt.show()

# ---- 6. Relatório Final ----
print(f"\nAUC da Curva ROC: {roc_auc:.2f}")

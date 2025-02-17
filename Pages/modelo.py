# -*- coding: utf-8 -*-
"""model

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1W6SoyXaLI2SLj03l2ULPwZ58sVAc29hO
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Garantia de que o model.py não tente configurar a página novamente

# Função para carregar os dados
@st.cache_data
def load_data():
    return pd.read_excel('https://github.com/MichaelJourdain93/Datathon_Passos_Magicos/raw/main/Datasets/dt_curated_passos_magicos.xlsx', engine='openpyxl')

df = load_data()

# Título e introdução
st.title("Dashboard Passos Mágicos: Transformando Vidas Através da Educação")
st.write("""
Bem-vindo ao dashboard interativo da ONG Passos Mágicos! Aqui, exploramos o impacto transformador
 de nossa organização na vida de jovens estudantes.
""")

# Visão geral dos dados
st.header("Nossa Jornada em Números")

# Calcular o total de alunos distintos (baseado na coluna 'Nome')
total_alunos = df['Nome'].nunique()  # Quantidade distinta de nomes

# Filtrar o DataFrame para remover duplicatas de nomes (garantir alunos únicos)
df_unique = df.drop_duplicates(subset='Nome')

# Calcular o percentual de masculino e feminino com base nos alunos únicos
gender_counts = df_unique['Gênero'].value_counts()
percent_masculino = (gender_counts.get('Masculino', 0) / total_alunos) * 100
percent_feminino = (gender_counts.get('Feminino', 0) / total_alunos) * 100

# Exibir as métricas
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de Estudantes", f"{total_alunos:,}")  # Usa a contagem distinta
col2.metric("Média de Idade", f"{df['Idade'].mean():.1f} anos")
col3.metric("INDE Médio", f"{df['INDE'].mean():.2f}")
col4.metric("Percentual Masculino", f"{percent_masculino:.1f}%")
col5.metric("Percentual Feminino", f"{percent_feminino:.1f}%")

# Correlação entre indicadores
st.subheader("Correlação entre Indicadores")

# Descrição do heatmap de correlação
st.write("""
**Um heatmap de correlação que exibe a relação entre diferentes indicadores e notas dos estudantes atendidos pela ONG "Passos Mágicos".**  
Cada célula do gráfico mostra o coeficiente de correlação entre dois indicadores ou notas, variando de **-1 a 1**, ou seja, da **menor correlação** a **maior**.
""")

# Ajuste o tamanho do heatmap
correlation_matrix = df[['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'IPP']].corr()
fig, ax = plt.subplots(figsize=(6, 4))  # Tamanho reduzido (8x6 polegadas)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax, fmt=".2f", linewidths=0.5)
st.pyplot(fig)

# Modelo preditivo
st.header("Modelo de Previsão de Sucesso")
X = df[['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'IPP']]
y = df['INDE']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

@st.cache_resource
def train_model():
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

model = train_model()

y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
st.write(f"Precisão do Modelo (R² Score): {r2:.2f}")

# Previsão interativa
st.subheader("Simulação de INDE Previsto")
inputs = {}
for col in X.columns:
    inputs[col] = st.slider(f"{col}", 0.0, 10.0, 5.0)
input_data = np.array([[inputs[col] for col in X.columns]])
prediction = model.predict(input_data)
#st.metric("INDE Previsto", f"{prediction[0]:.2f}")

# Classificação do INDE Previsto
def classify_inde(inde):
    if 2.405 <= inde < 5.506:
        return "Quartzo", "https://raw.githubusercontent.com/MichaelJourdain93/Datathon_Passos_Magicos/main/assets/images/quartzo.png"
    elif 5.506 <= inde < 6.868:
        return "Ágata", "https://raw.githubusercontent.com/MichaelJourdain93/Datathon_Passos_Magicos/main/assets/images/agata.png"
    elif 6.868 <= inde < 8.230:
        return "Ametista", "https://raw.githubusercontent.com/MichaelJourdain93/Datathon_Passos_Magicos/main/assets/images/ametista.png"
    elif 8.230 <= inde <= 9.294:
        return "Topázio", "https://raw.githubusercontent.com/MichaelJourdain93/Datathon_Passos_Magicos/main/assets/images/topazio.png"
    else:
        return "Fora da Classificação", None

# Classificação do INDE Previsto
classification, image_url = classify_inde(prediction[0])
st.subheader("Classificação do INDE Previsto")

# Exibir o INDE Previsto em azul e negrito
st.markdown(
    f"O INDE Previsto de <span style='color: blue; font-weight: bold;'>{prediction[0]:.2f}</span> é classificado como: **{classification}**",
    unsafe_allow_html=True
)

if image_url:
    # Ajuste o tamanho da imagem definindo a largura (width) em pixels
    st.image(image_url, caption=classification, width=400)  # Altere o valor de width conforme necessário
else:
    st.write("Fora da classificação.")

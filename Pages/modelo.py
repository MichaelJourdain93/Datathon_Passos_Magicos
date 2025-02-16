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
col1, col2, col3 = st.columns(3)
col1.metric("Total de Estudantes", f"{len(df):,}")
col2.metric("Média de Idade", f"{df['Idade'].mean():.1f} anos")
col3.metric("INDE Médio", f"{df['INDE'].mean():.2f}")

# Distribuição de gênero
gender_counts = df['Gênero'].value_counts()
st.subheader("Distribuição de Gênero")

# Ajuste o tamanho do gráfico de pizza para um tamanho bem pequeno
fig, ax = plt.subplots(figsize=(3, 3))  # Tamanho reduzido (3x3 polegadas)

# Gráfico de pizza com percentual e fonte ajustada
ax.pie(
    gender_counts.values, 
    labels=gender_counts.index, 
    autopct='%1.1f%%',  # Mantém o percentual
    colors=['#FF9999','#66B2FF'], 
    textprops={'fontsize': 6}  # Ajusta o tamanho da fonte dos rótulos e percentuais
)

# Exibir o gráfico no Streamlit
st.pyplot(fig)

# Correlação entre indicadores
st.subheader("Correlação entre Indicadores")

# Descrição do heatmap de correlação
st.write("""
**Um heatmap de correlação que exibe a relação entre diferentes indicadores e notas dos estudantes atendidos pela ONG "Passos Mágicos".**  
Cada célula do gráfico mostra o coeficiente de correlação entre dois indicadores ou notas, variando de **-1 a 1**, ou seja, da **menor correlação** a **maior**.
""")

# Ajuste o tamanho do heatmap
correlation_matrix = df[['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'IPP']].corr()
fig, ax = plt.subplots(figsize=(8, 6))  # Tamanho reduzido (8x6 polegadas)
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

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
fig, ax = plt.subplots()
ax.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%', colors=['#FF9999','#66B2FF'])
st.pyplot(fig)

# Correlação entre indicadores
st.subheader("Correlação entre Indicadores")
correlation_matrix = df[['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'IPP']].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
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
    elif 8.230 <= inde <= 10:
        return "Topázio", "https://raw.githubusercontent.com/MichaelJourdain93/Datathon_Passos_Magicos/main/assets/images/topazio.png"
    else:
        return "Fora da Classificação", None

classification, image_url = classify_inde(prediction[0])
st.subheader("Classificação do INDE Previsto")
st.write(f"O INDE Previsto de {prediction[0]:.2f} é classificado como: **{classification}**")

if image_url:
    st.image(image_url, caption=classification, use_container_width=True)  # Updated parameter
else:
    st.write("Fora da classificação.")

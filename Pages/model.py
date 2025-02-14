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

# Configuração da página
st.set_page_config(page_title="Dashboard Passos Mágicos", layout="wide")

# Carregar os dados
@st.cache_data
def load_data():
    return pd.read_excel('https://github.com/MichaelJourdain93/Datathon_Passos_Magicos/raw/main/Datasets/dt_curated_passos_magicos.xlsx', engine='openpyxl')

df = load_data()

# Título e introdução
st.title("Dashboard Passos Mágicos: Transformando Vidas Através da Educação")
st.write("""
Bem-vindo ao dashboard interativo da ONG Passos Mágicos! Aqui, exploramos o impacto transformador
de nossa organização na vida de jovens estudantes. Através de dados e visualizações, contamos a
história de como estamos fazendo a diferença na educação e no futuro de nossa comunidade.
""")

# Visão geral dos dados
st.header("Nossa Jornada em Números")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Estudantes", f"{len(df):,}")
col2.metric("Média de Idade", f"{df['Idade'].mean():.1f} anos")
col3.metric("INDE Médio", f"{df['INDE'].mean():.2f}")

# Distribuição de gênero
st.subheader("Diversidade é Nossa Força: Distribuição de Gênero")
gender_counts = df['Gênero'].value_counts()
fig, ax = plt.subplots()
ax.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%', colors=['#FF9999','#66B2FF'])
ax.set_title("Distribuição de Gênero dos Estudantes")
st.pyplot(fig)
st.write("""
Nosso programa abraça a diversidade, atendendo estudantes de todos os gêneros. Esta distribuição
equilibrada reflete nosso compromisso com a igualdade de oportunidades na educação.
""")

# Distribuição de idade
st.subheader("Impactando Todas as Idades: Perfil Etário dos Estudantes")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df['Idade'], bins=20, kde=True, ax=ax, color='#66B2FF')
ax.set_title("Distribuição de Idade dos Estudantes")
ax.set_xlabel("Idade")
ax.set_ylabel("Número de Estudantes")
st.pyplot(fig)
st.write("""
Atendemos uma ampla faixa etária, desde crianças até jovens adultos. Cada barra representa uma
história única de crescimento e aprendizado. Esta diversidade nos permite criar programas
personalizados para cada fase do desenvolvimento educacional.
""")

# Correlação entre indicadores
st.subheader("Desvendando o Sucesso: Correlação entre Indicadores")
correlation_matrix = df[['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'IPP']].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Mapa de Calor da Correlação entre Indicadores")
st.pyplot(fig)
st.write("""
Este mapa de calor revela as intrincadas relações entre nossos indicadores de desempenho. As cores
mais quentes indicam correlações positivas fortes, mostrando como diferentes aspectos do
desenvolvimento dos estudantes estão interligados. Esta visão nos ajuda a entender melhor como
podemos impactar positivamente múltiplas áreas da vida de nossos estudantes.
""")

# Modelo preditivo
st.header("Prevendo o Futuro: Nosso Modelo de Sucesso")

# Preparar os dados para o modelo
X = df[['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'IPP']]
y = df['INDE']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
@st.cache_resource
def train_model():
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

model = train_model()

# Fazer previsões e avaliar o modelo
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

st.write(f"Precisão do Modelo (R² Score): {r2:.2f}")
st.write("""
Nosso modelo preditivo, baseado em Random Forest, nos permite antecipar o Índice de Desenvolvimento
Educacional (INDE) de nossos estudantes com uma precisão notável. Isso nos ajuda a personalizar
nossa abordagem para cada aluno, garantindo que possamos oferecer o suporte necessário onde é mais
necessário.
""")

# Importância das features
feature_importance = pd.DataFrame({'feature': X.columns, 'importance': model.feature_importances_})
feature_importance = feature_importance.sort_values('importance', ascending=False)

st.subheader("Os Pilares do Nosso Sucesso: Importância dos Indicadores")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='importance', y='feature', data=feature_importance, ax=ax, palette='viridis')
ax.set_title("Importância dos Indicadores para o INDE")
ax.set_xlabel("Importância")
ax.set_ylabel("Indicador")
st.pyplot(fig)
st.write(f"""
Os três indicadores mais importantes para o sucesso de nossos estudantes são:
1. {feature_importance.iloc[0]['feature']} (Importância: {feature_importance.iloc[0]['importance']:.2f})
2. {feature_importance.iloc[1]['feature']} (Importância: {feature_importance.iloc[1]['importance']:.2f})
3. {feature_importance.iloc[2]['feature']} (Importância: {feature_importance.iloc[2]['importance']:.2f})

Estes indicadores são os pilares do nosso programa, guiando nossas estratégias para maximizar o
impacto positivo na vida de cada estudante.
""")

# Previsão interativa
st.subheader("Simule o Futuro: Faça uma Previsão")
st.write("""
Use os controles abaixo para simular diferentes cenários e ver como eles afetariam o INDE de um
estudante. Esta ferramenta nos ajuda a entender melhor como diferentes fatores interagem para
influenciar o desenvolvimento educacional.
""")

col1, col2 = st.columns(2)
with col1:
    iaa = st.slider("Índice de Aproveitamento Acadêmico (IAA)", 0.0, 10.0, 5.0)
    ieg = st.slider("Índice de Engajamento (IEG)", 0.0, 10.0, 5.0)
    ips = st.slider("Índice Psicossocial (IPS)", 0.0, 10.0, 5.0)
    ida = st.slider("Índice de Desempenho Acadêmico (IDA)", 0.0, 10.0, 5.0)
with col2:
    ipv = st.slider("Índice do Ponto de Virada (IPV)", 0.0, 10.0, 5.0)
    ian = st.slider("Índice de Adequação de Nível (IAN)", 0.0, 10.0, 5.0)
    ipp = st.slider("Índice de Progresso Pessoal (IPP)", 0.0, 10.0, 5.0)

input_data = np.array([[iaa, ieg, ips, ida, ipv, ian, ipp]])
prediction = model.predict(input_data)

st.metric("INDE Previsto", f"{prediction[0]:.2f}")

# Conclusão
st.header("Nossa Visão para o Futuro")
st.write("""
Com base em nossa análise de dados e insights obtidos, podemos concluir que:

1. A ONG "Passos Mágicos" está tendo um impacto positivo significativo no desenvolvimento educacional
   dos estudantes, como evidenciado pelas correlações positivas entre os indicadores-chave.
2. Nossa abordagem diversificada, atendendo diferentes faixas etárias e gêneros, nos permite criar
   um ambiente inclusivo e adaptado às necessidades individuais.
3. O foco nos indicadores mais importantes, como identificado pelo nosso modelo preditivo, nos
   permite direcionar recursos e esforços de forma mais eficiente.

Olhando para o futuro, planejamos:
1. Desenvolver programas personalizados baseados nos indicadores mais impactantes para cada faixa etária.
2. Implementar um sistema de monitoramento contínuo usando nosso modelo preditivo para identificar
   e apoiar estudantes que possam precisar de atenção adicional.
3. Expandir nossas parcerias com escolas e comunidades para ampliar nosso alcance e impacto.

Juntos, estamos construindo um futuro mais brilhante, um estudante de cada vez. Obrigado por fazer
parte desta jornada transformadora com a Passos Mágicos!
""")

# Sidebar com filtros
st.sidebar.header("Explore Nossos Dados")
st.sidebar.write("Use os filtros abaixo para analisar grupos específicos de estudantes.")
selected_gender = st.sidebar.multiselect("Gênero", df['Gênero'].unique())
selected_age = st.sidebar.slider("Faixa Etária", int(df['Idade'].min()), int(df['Idade'].max()), (int(df['Idade'].min()), int(df['Idade'].max())))

# Aplicar filtros
filtered_df = df
if selected_gender:
    filtered_df = filtered_df[filtered_df['Gênero'].isin(selected_gender)]
filtered_df = filtered_df[(filtered_df['Idade'] >= selected_age[0]) & (filtered_df['Idade'] <= selected_age[1])]

# Atualizar visualizações com dados filtrados
st.header("Análise Personalizada")
st.write(f"Mostrando dados para {len(filtered_df)} estudantes com base nos filtros selecionados.")
st.dataframe(filtered_df)

# Gráfico adicional baseado nos filtros
st.subheader("INDE por Idade (Dados Filtrados)")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=filtered_df, x='Idade', y='INDE', hue='Gênero', ax=ax)
ax.set_title("INDE vs Idade (Dados Filtrados)")
st.pyplot(fig)
st.write("""
Este gráfico mostra a relação entre idade e INDE para o grupo selecionado. Cada ponto representa um
estudante, permitindo-nos visualizar tendências e padrões específicos dentro dos critérios escolhidos.
""")
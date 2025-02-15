## -*- coding: utf-8 -*-
"""analysis

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FWRQbp8jWBVK_ezjF7g9EDJpwimgadGa
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import globals
import graficos
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração inicial do Streamlit (DEVE SER O PRIMEIRO COMANDO STREAMLIT)
st.set_page_config(layout="wide")

# Carregar os dados
df = pd.read_excel('https://github.com/MichaelJourdain93/Datathon_Passos_Magicos/raw/main/Datasets/dt_curated_passos_magicos.xlsx', engine='openpyxl')

# Título
title = "📊 Análise dos Dados da ONG Passos Mágicos"
st.title(title)

# Mostrar os primeiros dados
st.subheader("Visualização dos Dados")

tab1, tab2 = st.tabs(['Indicadores', 'Análises'])

with tab1:
    cbAno = st.selectbox('Selecione o Ano:', list(globals.lAno.keys()), key="cbAno")

    df_ano = globals.df
    if cbAno != 'Todos':
        df_ano = globals.df[globals.df['ANO'] == globals.lAno[cbAno]]
        if globals.lAno[cbAno] > 2022:
            df_ano_anterior = globals.df[globals.df['ANO'] == globals.lAno[cbAno] - 1]

    num_colunas_pedras = len(globals.lPedras)
    colunas_2 = st.columns(num_colunas_pedras)
    for i, dados in enumerate(globals.lPedras):
        coluna_atual = colunas_2[i % num_colunas_pedras]
        with coluna_atual:
            if cbAno != 'Todos' and globals.lAno[cbAno] > 2022:
                st.metric(dados, np.sum(df_ano['PEDRA'] == dados), delta=int(np.sum(df_ano['PEDRA'] == dados) - np.sum(df_ano_anterior['PEDRA'] == dados)))
            else:
                st.metric(dados, np.sum(df_ano['PEDRA'] == dados), delta=None)

    num_colunas = len(globals.lIndicadores_1)
    colunas_1 = st.columns(num_colunas, border=True)

    for i, dados in enumerate(globals.lIndicadores_1):
        coluna_atual = colunas_1[i % num_colunas]
        with coluna_atual:
            st.subheader(dados, help='Comparativo em relação ao ano anterior')
            if(cbAno != 'Todos' and globals.lAno[cbAno] > 2022):
                st.metric('Média:', df_ano[dados].mean().round(2), border=False, delta=round(df_ano[dados].mean().round(2) - df_ano_anterior[dados].mean().round(2),2))
                st.metric('Mediana:', df_ano[dados].median().round(2), border=False, delta=round(df_ano[dados].median().round(2) - df_ano_anterior[dados].median().round(2),2))
                st.metric('Min:', df_ano[dados].min().round(2), border=False, delta=round(df_ano[dados].min().round(2) - df_ano_anterior[dados].min().round(2),2))
                st.metric('Max:', df_ano[dados].max().round(2), border=False, delta=round(df_ano[dados].max().round(2) - df_ano_anterior[dados].max().round(2), 2))
            else:
                st.metric('Média:', df_ano[dados].mean().round(2),border=False, delta=None, delta_color='off')
                st.metric('Mediana:', df_ano[dados].median().round(2),border=False, delta=None, delta_color='off')
                st.metric('Min:', df_ano[dados].min().round(2),border=False, delta=None, delta_color='off')
                st.metric('Max:', df_ano[dados].max().round(2),border=False, delta=None, delta_color='off')

# Análise descritiva básica
with tab2:
    st.subheader("Distribuição dos Alunos por Gênero")
    fig, ax = plt.subplots(figsize=(10, 6))
    df['Gênero'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title('Distribuição dos Alunos por Gênero')
    ax.set_xlabel('Gênero')
    ax.set_ylabel('Número de Alunos')
    st.pyplot(fig)

    st.subheader("Distribuição dos Alunos por Fase")
    fig, ax = plt.subplots(figsize=(12, 6))
    df['Fase'].value_counts().sort_index().plot(kind='bar', ax=ax)
    ax.set_title('Distribuição dos Alunos por Fase')
    ax.set_xlabel('Fase')
    ax.set_ylabel('Número de Alunos')
    st.pyplot(fig)

    st.subheader("Relação entre INDE e IDA")
    fig = px.scatter(df, x='INDE', y='IDA', color='Pedra', hover_data=['Nome', 'Fase', 'Idade'])
    st.plotly_chart(fig)

    st.subheader("Distribuição das Notas por Disciplina")
    fig, ax = plt.subplots(figsize=(12, 6))
    df[['Mat', 'Por', 'Ing']].boxplot(ax=ax)
    ax.set_title('Distribuição das Notas por Disciplina')
    ax.set_ylabel('Notas')
    st.pyplot(fig)

    st.subheader("Mapa de Correlação entre Indicadores e Notas")
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(df[['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'IPP', 'Mat', 'Por', 'Ing']].corr(), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Mapa de Correlação')
    st.pyplot(fig)

    st.subheader("Distribuição de Pedras por Fase")
    pedra_fase = pd.crosstab(df['Fase'], df['Pedra'])
    fig = go.Figure(data=[
        go.Bar(name=pedra, x=pedra_fase.index, y=pedra_fase[pedra]) for pedra in pedra_fase.columns
    ])
    fig.update_layout(barmode='stack', title='Distribuição de Pedras por Fase')
    st.plotly_chart(fig)

    st.subheader("Comparação dos Indicadores Médios por Pedra")
    indicadores = ['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'IPP']
    medias_por_pedra = df.groupby('Pedra')[indicadores].mean()
    fig = go.Figure()
    for pedra in medias_por_pedra.index:
        fig.add_trace(go.Scatterpolar(
            r=medias_por_pedra.loc[pedra],
            theta=indicadores,
            fill='toself',
            name=pedra
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        title='Comparação dos Indicadores Médios por Pedra'
    )
    st.plotly_chart(fig)

    st.subheader("Evolução do INDE ao Longo dos Anos")
    df['Ano Letivo'] = pd.to_datetime(df['Ano Letivo'], format='%Y')
    inde_por_ano = df.groupby('Ano Letivo')['INDE'].mean().reset_index()
    fig = px.line(inde_por_ano, x='Ano Letivo', y='INDE', title='Evolução do INDE ao Longo dos Anos')
    st.plotly_chart(fig)

# Storytelling
st.subheader("Storytelling: Impacto da ONG Passos Mágicos")
st.write("A análise dos dados da ONG Passos Mágicos revela insights importantes sobre o impacto do programa:")
st.write("**1. Diversidade de Atendimento:**")
st.write(f"- A ONG atende {df['Gênero'].nunique()} gêneros diferentes.")
st.write(f"- Os alunos estão distribuídos em {df['Fase'].nunique()} fases diferentes, mostrando a amplitude do programa.")

st.write("**2. Desempenho Acadêmico:**")
st.write(f"- A média do IDA (Indicador de Desempenho Acadêmico) é {df['IDA'].mean():.2f}.")
st.write(f"- Correlação positiva de {df['INDE'].corr(df['IDA']):.2f} entre INDE e IDA.")

st.write("**3. Engajamento e Desenvolvimento:**")
st.write(f"- IEG médio: {df['IEG'].mean():.2f}, indicando bom nível de participação.")
st.write(f"- IPV médio: {df['IPV'].mean():.2f}, mostrando progresso significativo.")

st.write("**4. Impacto por Tipo de Instituição:**")
instituicoes = df.groupby('Instituição de ensino')['IDA'].mean().sort_values(ascending=False)
st.write(f"- Maior IDA médio: '{instituicoes.index[0]}' com {instituicoes.iloc[0]:.2f}.")
st.write(f"- Menor IDA médio: '{instituicoes.index[-1]}' com {instituicoes.iloc[-1]:.2f}.")

st.write("**5. Evolução ao Longo do Tempo:**")
inde_inicial = inde_por_ano['INDE'].iloc[0]
inde_final = inde_por_ano['INDE'].iloc[-1]
variacao_inde = (inde_final - inde_inicial) / inde_inicial * 100
st.write(f"- O INDE médio variou de {inde_inicial:.2f} para {inde_final:.2f}, uma mudança de {variacao_inde:.2f}%.")

st.write("**Conclusão:**")
st.write("A análise demonstra que a ONG Passos Mágicos tem um impacto positivo significativo na vida dos estudantes atendidos. O programa melhora o desempenho acadêmico e promove o engajamento e desenvolvimento pessoal.")

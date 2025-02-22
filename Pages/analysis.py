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

# Carregar os dados
df = pd.read_excel('https://github.com/MichaelJourdain93/Datathon_Passos_Magicos/raw/main/Datasets/dt_curated_passos_magicos.xlsx', engine='openpyxl')

# Título da Página
st.title("📊 Análise dos Dados da ONG Passos Mágicos")

# Mostrar os primeiros dados
st.subheader("Visualização dos Dados")

tab1, tab2 , tab3  = st.tabs(['Indicadores', 'Análises', 'Observações'])

with tab1:
    cbAno = st.selectbox('Selecione o Ano:', list(globals.lAno.keys()), key="cbAno")
    df_ano = globals.df
    if cbAno != 'Todos':
        df_ano = globals.df[globals.df['Ano Letivo'] == globals.lAno[cbAno]]
        if globals.lAno[cbAno] > 2022:
            df_ano_anterior = globals.df[globals.df['Ano Letivo'] == globals.lAno[cbAno] - 1]

    num_colunas_pedras = len(globals.lPedras)
    colunas_2 = st.columns(num_colunas_pedras)
    for i, dados in enumerate(globals.lPedras):
        coluna_atual = colunas_2[i % num_colunas_pedras]
        with coluna_atual:
            if cbAno != 'Todos' and globals.lAno[cbAno] > 2022:
                st.metric(dados, np.sum(df_ano['Pedra'] == dados), delta=int(np.sum(df_ano['Pedra'] == dados) - np.sum(df_ano_anterior['Pedra'] == dados)))
            else:
                st.metric(dados, np.sum(df_ano['Pedra'] == dados), delta=None)
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
        st.header("Análise Descritiva")
        
        # Distribuição dos Alunos por Gênero
        st.subheader("Distribuição dos Alunos por Gênero")
        # Criar DataFrame com alunos únicos (sem duplicatas de nome)
        df_unique = df.drop_duplicates(subset='Nome')

        # Plotar o gráfico com base nos alunos únicos
        fig, ax = plt.subplots(figsize=(12, 4))
        df_unique['Gênero'].value_counts().plot(kind='bar', ax=ax, color=['skyblue', 'lightcoral'])
        ax.set_xlabel('Gênero')
        ax.set_ylabel('Número de Alunos (Únicos)')  # Legenda atualizada para refletir a mudança
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        st.pyplot(fig)

    
        st.write("""
        O número de alunos do gênero **feminino** (57%) é ligeiramente maior do que o do gênero **masculino**(43%),
        . Essa distribuição sugere uma relativa paridade entre os gêneros, indicando que não há uma grande disparidade significativa na quantidade
        de alunos entre homens e mulheres.
        """)
    
        # Distribuição de Alunos por Fase Educacional
        st.subheader("Distribuição de Alunos por Fase Educacional")
        fig, ax = plt.subplots(figsize=(12, 6))
        df['Fase'].value_counts().sort_index().plot(kind='bar', ax=ax, color='lightgreen')
        ax.set_xlabel('Fase')
        ax.set_ylabel('Número de Alunos')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        st.pyplot(fig)
    
        st.write("""
        A maior parte dos alunos está nas fases iniciais (0 a 3), representando cerca de 55% do total.
        A fase 0 sozinha corresponde a aproximadamente 22%. Conforme a progressão, há uma queda no número de alunos:
        as fases intermediárias (4 a 6) concentram 16%, e as finais (7 a 9) apenas 7%. Isso indica uma possível dificuldade
        na retenção e progressão dos estudantes. A ONG 'Passos Mágicos' pode direcionar estratégias para incentivar a continuidade
        dos estudos e minimizar a evasão nas fases mais avançadas.
        """)
    
        # Distribuição de Alunos por Idade
        st.subheader("Distribuição de Alunos por Idade")
       # Criar DataFrame com alunos únicos (sem duplicatas de nome)
        df_unique = df.drop_duplicates(subset='Nome')

        # Plotar o gráfico com base nos alunos únicos
        fig, ax = plt.subplots(figsize=(10, 6))
        age_counts = df_unique['Idade'].value_counts().sort_index()
        age_counts.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_xlabel('Idade')
        ax.set_ylabel('Número de Alunos (Únicos)')  # Legenda atualizada
        ax.set_xticks(range(len(age_counts)))
        ax.set_xticklabels(age_counts.index, rotation=45)
        st.pyplot(fig)
    
        st.write("""
        - A maior concentração de alunos está na faixa etária de **12 anos**, seguida por **11 e 13 anos**.
        - O número de alunos diminui drasticamente a partir dos **17 e 18 anos**, indicando maior evasão ou menor retenção em idades mais avançadas.
        - Esses dados reforçam a importância de intervenções direcionadas para alunos mais velhos, que apresentam maior defasagem e menor presença no programa.
        """)
    
        # Relação entre Idade e INDE por Fase
        st.subheader("Relação entre Idade e INDE por Fase")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.scatterplot(x='Idade', y='INDE', hue='Fase', data=df, palette='tab10', ax=ax)
        ax.set_xlabel('Idade')
        ax.set_ylabel('INDE')
        ax.legend(title='Fase', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)
    
        st.write("""
        As fases iniciais concentram alunos mais jovens, enquanto as fases intermediárias e avançadas apresentam maior diversidade de faixas etárias.
        Isso reflete o esforço da ONG em atender alunos com diferentes níveis de aprendizado, mas também destaca a necessidade de suporte para alunos fora da faixa etária padrão.
        """)
    
        # Relação entre Idade e INDE por Gênero
        st.subheader("Relação entre Idade e INDE por Gênero")
        fig = px.scatter(df, x='Idade', y='INDE', color='Gênero')
        st.plotly_chart(fig)
    
        st.write("""
        **Relação entre Idade e INDE**: Observa-se que o **INDE** varia pouco com a idade, mas alunos mais jovens (até **15 anos**) apresentam maior concentração de valores altos.
        Além disso, não há diferenças significativas entre os gêneros em termos de desenvolvimento educacional, embora as meninas apresentem, em geral, um desempenho ligeiramente melhor.
        """)
    
        # Defasagem por Idade
        st.subheader("Defasagem por Idade")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='Idade', y='Defasagem', data=df, ci=None, palette='viridis', ax=ax)
        ax.set_xlabel('Idade')
        ax.set_ylabel('Defasagem (anos)')
        ax.set_xticklabels(df['Idade'], rotation=45)
        st.pyplot(fig)
    
        st.write("""
        1. **Defasagem Negativa em Idades Mais Jovens**: Alunos com idades entre **10 e 15 anos** apresentam, em média, defasagem negativa (valores abaixo de 0), indicando que estão adiantados em relação à fase ideal para sua idade.
        2. **Defasagem Positiva em Idades Mais Avançadas**: A partir dos **18 anos**, a defasagem média começa a aumentar significativamente, atingindo valores positivos altos (acima de 0). Isso sugere que alunos mais velhos estão atrasados em relação à fase educacional esperada.
        3. **Transição Crítica**: Entre as idades de **16 e 17 anos**, a defasagem se aproxima de zero, marcando uma transição entre alunos adiantados e atrasados. Esse padrão reflete desafios específicos enfrentados por alunos mais velhos e destaca a necessidade de intervenções direcionadas para reduzir a defasagem nas idades mais avançadas.
        """)
    
        # Relação entre Defasagem e INDE por Fase
        st.subheader("Relação entre Defasagem e INDE por Fase")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.scatterplot(x='Defasagem', y='INDE', hue='Fase', data=df, palette='tab10', ax=ax)
        ax.set_xlabel('Defasagem (anos)')
        ax.set_ylabel('INDE')
        ax.legend(title='Fase', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)
    
        st.write("""
        Alunos com maior defasagem (idade superior à fase ideal) apresentam valores mais baixos de **INDE**, indicando que a defasagem impacta negativamente o desenvolvimento educacional.
        No entanto, alunos com defasagem próxima de **zero** tendem a ter melhores indicadores.
        """)
    
        # Relação entre INDE e IDA
        st.subheader("Relação entre INDE e IDA")
        fig = px.scatter(df, x='INDE', y='IDA', color='Pedra', hover_data=['Nome', 'Fase', 'Idade'])
        st.plotly_chart(fig)
    
        st.write("""
        A relação entre **INDE** (Indicador de Desenvolvimento Educacional) e **IDA** (Indicador de Desempenho Acadêmico) apresenta uma correlação positiva clara.
        À medida que o **INDE** aumenta, o **IDA** também tende a crescer, indicando que um maior desenvolvimento educacional está associado a melhores desempenhos acadêmicos.
        A dispersão dos pontos sugere variações individuais, mas a tendência geral é consistente.
        """)
    
        # Distribuição das Notas por Disciplina
        st.subheader("Distribuição das Notas por Disciplina")
        fig, ax = plt.subplots(figsize=(12, 6))
        df[['Mat', 'Por', 'Ing']].boxplot(ax=ax)
        ax.set_ylabel('Notas')
        st.pyplot(fig)
    
        st.write("""
        As medianas das três disciplinas são semelhantes (em torno de **6 a 7**), com **Inglês** apresentando uma distribuição ligeiramente mais alta.
        No entanto, todas as disciplinas têm **outliers significativos** em notas muito baixas, indicando que alguns alunos enfrentam dificuldades específicas.
        A amplitude das notas é maior em **Matemática** e **Português** do que em Inglês.
        """)
    
        # Mapa de Correlação entre Indicadores e Notas
        st.subheader("Mapa de Correlação entre Indicadores e Notas")
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(df[['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'IPP', 'Mat', 'Por', 'Ing']].corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Mapa de Correlação')
        st.pyplot(fig)
    
        st.write("""
        O heatmap de correlação revela as relações entre diferentes indicadores e notas dos estudantes atendidos pela ONG "Passos Mágicos". As correlações variam de -1 (menor correlação) a 1 (maior correlação).
        Entre os destaques, o **IDA** (Indicador de Desempenho Acadêmico) apresenta forte correlação com as notas em Matemática (0.85), Português (0.82) e Inglês (0.90), confirmando que o desempenho acadêmico
        é influenciado diretamente pelas disciplinas. Além disso, o **INDE** (Indicador de Desenvolvimento Educacional) tem alta correlação com o **IEG** (Indicador de Engajamento), sugerindo que maior engajamento
        está associado a melhores resultados educacionais.
    
        Outros insights incluem a moderada influência do **IPS** (Indicador Psicossocial) no desenvolvimento educacional e nos pontos de virada, e a baixa correlação do **IAN** (Indicador de Adequação de Nível) com
        outros indicadores. As notas das três disciplinas possuem alta correlação entre si, indicando que bons desempenhos tendem a ser consistentes em todas as áreas. Estratégias práticas devem focar no aumento do
        engajamento (**IEG**), que está fortemente relacionado ao desenvolvimento educacional (**INDE**) e ao desempenho acadêmico (**IDA**).
        """)
    
        # Relação entre INDE e IDA por Tipo de Pedra
        st.subheader("Relação entre INDE e IDA por Tipo de Pedra")
        fig = px.scatter(df, x='INDE', y='IDA', color='Pedra', hover_data=['Nome', 'Fase', 'Idade'])
        fig.update_layout(title='Relação entre INDE e IDA por Tipo de Pedra')
        st.plotly_chart(fig)
    
        st.write("""
        A relação entre INDE e IDA é consistente entre os diferentes tipos de pedra (Quartzo, Ametista, Ágata, Topázio), mas as categorias com maior densidade nas faixas
        superiores de INDE e IDA (como Ametista e Topázio) sugerem que esses grupos apresentam melhores desempenhos gerais.
        """)
    
        # Distribuição de Pedras por Fase
        st.subheader("Distribuição de Pedras por Fase")
        pedra_fase = pd.crosstab(df['Fase'], df['Pedra'])
        fig = go.Figure(data=[
            go.Bar(name=pedra, x=pedra_fase.index, y=pedra_fase[pedra]) for pedra in pedra_fase.columns
        ])
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)
    
        st.write("""
        1. **Distribuição por Fase**:
        A maioria dos alunos está concentrada nas fases iniciais (0, 1, 2 e 3), com uma redução progressiva nas fases mais avançadas. Isso indica que o programa da ONG tem
        maior impacto nas etapas iniciais de formação.
    
        2. **Distribuição por Pedra**:
        As categorias de pedra (Topázio, Quartzo, Ametista e Ágata) estão bem representadas em todas as fases iniciais, mas a presença diminui significativamente nas fases
        finais. Topázio e Quartzo dominam as fases intermediárias, enquanto Ágata tem maior destaque nas fases finais (como a fase 8). Isso pode refletir diferentes níveis de
        desempenho ou engajamento ao longo do tempo.
        """)
    
        # Comparação dos Indicadores Médios por Pedra
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
        )
        st.plotly_chart(fig)
    
        st.write("""
        As categorias de pedra apresentam desempenhos médios semelhantes em todos os indicadores, com destaque para **IEG** (Indicador de Engajamento) e **INDE** (Indicador de Desenvolvimento Educacional),
        que possuem valores mais elevados. Isso sugere que o engajamento está fortemente alinhado ao desenvolvimento educacional.
        """)
    
        # Evolução do INDE ao Longo dos Anos
        st.subheader("Evolução do INDE ao Longo dos Anos")
        df['Ano Letivo'] = pd.to_datetime(df['Ano Letivo'], format='%Y')
        inde_por_ano = df.groupby('Ano Letivo')['INDE'].mean().reset_index()
        fig = px.line(inde_por_ano, x='Ano Letivo', y='INDE')
        st.plotly_chart(fig)
    
        st.write("""
        O INDE apresenta um crescimento constante até o início de 2023, seguido por uma queda gradual. Isso indica que houve avanços significativos no desenvolvimento educacional no período inicial,
        mas desafios surgiram posteriormente, possivelmente relacionados a mudanças no programa ou fatores externos.
        """)
    
        # Análises de Indicadores Acadêmicos e Engajamento por Instituição de Ensino
        st.subheader("Análises de Indicadores Acadêmicos e Engajamento por Instituição de Ensino")
        fig1 = px.box(df, x='Instituição de ensino', y='IDA')
        st.plotly_chart(fig1)
    
        st.write("""
        Alunos de instituições privadas com programas de bolsas apresentam **IDA mais alto** em comparação com escolas públicas ou redes convencionais.
        Isso evidencia o impacto positivo de iniciativas direcionadas, como bolsas e programas de apadrinhamento, no desempenho acadêmico.
        """)
    
        # Relação entre Engajamento (IEG) e Ponto de Virada (IPV)
        st.subheader("Relação entre Engajamento (IEG) e Ponto de Virada (IPV)")
        fig2 = px.scatter(df, x='IEG', y='IPV', color='Pedra', hover_data=['Nome', 'Fase'])
        st.plotly_chart(fig2)
    
        st.write("""
        Há uma **correlação positiva** entre o IEG (Indicador de Engajamento) e o IPV (Indicador de Ponto de Virada).
        À medida que o engajamento aumenta, os pontos de virada também tendem a crescer, indicando que maior engajamento está associado a momentos significativos de progresso no desenvolvimento dos alunos.
    
        - **Distribuição por Pedras**: Ametista e Topázio predominam nos níveis mais altos de engajamento (**IEG > 8**) e ponto de virada (**IPV > 8**), sugerindo maior desempenho. Já Quartzo e Ágata estão mais concentrados em níveis médios, indicando áreas para melhoria.
        - **Concentração de Dados**: A maioria dos alunos apresenta valores intermediários de IEG (**entre 5 e 8**) e IPV (**entre 4 e 8**), refletindo um bom nível geral de engajamento e impacto, mas com espaço para impulsionar os extremos superiores.
        """)
        
# Storytelling
with tab3:
    st.subheader("Impacto da ONG Passos Mágicos")
    st.write("A análise dos dados da ONG Passos Mágicos revela insights importantes sobre o impacto do programa:")
    st.write("**1. Diversidade de Atendimento:**")
    st.write(f"- A ONG atende {df['Gênero'].nunique()} gêneros diferentes.")
    st.write(f"- Os alunos estão distribuídos em {df['Fase'].nunique()} fases diferentes, mostrando a amplitude do programa.")
    st.write(" - Os alunos da fase 9 podem ser facilmente assimilados aos da fase 8, segundo o comportamento do seus dados ")

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

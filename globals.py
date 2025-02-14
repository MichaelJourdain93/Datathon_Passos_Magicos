import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/Rogeriom49/datathon_fiap/refs/heads/main/datasets/alunos_2.csv')

df_model_report = pd.read_csv('https://raw.githubusercontent.com/Rogeriom49/datathon_fiap/refs/heads/main/datasets/model_resport.csv', sep=';')

sUrl =  'https://raw.githubusercontent.com/Rogeriom49/datathon_fiap/refs/heads/main/best_model_random_forest.pkl'

lAno = {'Todos': 'Todos','2020': 2020, '2021': 2021, '2022':2022}

lIndicadores_1 = ['INDE', 'IAA', 'IEG','IPS','IDA', 'IPP', 'IPV','IAN']

lPedras = ['Topázio', 'Ametista', 'Ágata', 'Quartzo']

repo_url = 'https://github.com/Rogeriom49/datathon_fiap'
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/MichaelJourdain93/Datathon_Passos_Magicos/refs/heads/main/Datasets/dt_curated_passos_magicos_.csv')

df_model_report = pd.read_csv('https://raw.githubusercontent.com/MichaelJourdain93/Datathon_Passos_Magicos/refs/heads/main/Notebook/model_passosmag.csv', sep=';')

sUrl =  'https://github.com/MichaelJourdain93/Datathon_Passos_Magicos/blob/main/best_model_logistic_regression.pkl'

lAno = {'Todos': 'Todos','2022': 2022, '2023': 2023, '2024':2024}

lIndicadores_1 = ['INDE', 'IAA', 'IEG','IPS','IDA', 'IPP', 'IPV','IAN']

lPedras = ['Topázio', 'Ametista', 'Ágata', 'Quartzo']

repo_url = 'https://github.com/MichaelJourdain93/Datathon_Passos_Magicos'

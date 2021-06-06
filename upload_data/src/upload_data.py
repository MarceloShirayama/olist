import os
import pandas as pd
from olistlib.db import utils

# diretórios do projeto
BASE_DIR = os.path.dirname(
    os.path.dirname((os.path.abspath(__file__)))
)
DATA_DIR = os.path.join(BASE_DIR, 'data')

# lista de arquivos no diretório data
list_files_data = os.listdir(DATA_DIR)
# apenas os arquivos .csv
files_csv = [file for file in list_files_data if file.endswith('.csv')]

# conexão com o banco de dados
connection = utils.connect_db('sqlite', DATA_DIR)

# importar cada arquivo csv para uma tabela do banco de dados
for file in files_csv:
    df = pd.read_csv(os.path.join(DATA_DIR, file))
    table_name = 'tb_' + \
        file.replace('olist_', '').replace('_dataset', '').replace('.csv', '')
    df.to_sql(table_name, connection, if_exists='replace', index=False)
    print(f'criando tabela: {table_name}')

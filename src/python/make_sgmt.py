import os
import pandas as pd
import sqlalchemy
import argparse
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

# diretórios do projeto
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')

# importa a query sql
with open(os.path.join(SQL_DIR, 'segmentos.sql')) as query_file:
    sql_query = query_file.read()

# insere as datas de início e fim do período de consulta da query sql
parser = argparse.ArgumentParser()
# parser.add_argument('--date_init', '-i', help='Data de início da extração', default='')
parser.add_argument('--date_end', '-e', help='Data de fim da extração', default='2018-06-01')
args = parser.parse_args()
date_end = args.date_end
year = int(date_end.split('-')[0]) - 1
month = int(date_end.split('-')[1])
date_init = f'{year}-{month}-01'
sql_query = sql_query.format(
    date_init=date_init, date_end=date_end
)

# configurações do banco de dados sqlite
db_name = os.path.join(DATA_DIR, 'olist')
str_connection = f'sqlite:///{db_name}.db'
# abrir conexão com o banco de dados sqlite
connection = sqlalchemy.create_engine(str_connection)

create_sql_query = f'''CREATE TABLE tb_seller_sgmt AS {sql_query};'''

insert_sql_query = f'''
    DELETE FROM tb_seller_sgmt WHERE dt_sgmt = '{date_end}';
    INSERT INTO tb_seller_sgmt {sql_query};
'''

try:
    print('Criando tabela...')
    connection.execute(create_sql_query)
    print('tabela criada com sucesso!')
except SQLAlchemyError as err:
    print(err._message)
    print(f'Inserindo dados de segmentação de {date_init} a {date_end}...')
    for q in insert_sql_query.split(';')[:-1]:
        connection.execute(q)
    print('Dados inseridos com sucesso!')

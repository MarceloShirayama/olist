import os
import argparse
from sqlalchemy.exc import SQLAlchemyError
import utils

# diretórios do projeto
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')

# importa a query sql
sql_query = utils.import_query(os.path.join(SQL_DIR, 'segmentos.sql'))

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

# # abrir conexão com o banco de dados sqlite
conn = utils.connect_db()

create_sql_query = f'''CREATE TABLE tb_seller_sgmt AS {sql_query};'''

insert_sql_query = f'''
    DELETE FROM tb_seller_sgmt WHERE dt_sgmt = '{date_end}';
    INSERT INTO tb_seller_sgmt {sql_query};
'''

# excecução da query
try:
    print('Criando tabela...')
    utils.execute_many_sql_query(create_sql_query, conn)
    print('tabela criada com sucesso!')
except SQLAlchemyError:
    # print(err._message)
    print(f'Inserindo dados de segmentação de {date_init} a {date_end}...')
    utils.execute_many_sql_query(insert_sql_query, conn, verbose=True)
    print('Dados inseridos com sucesso!')

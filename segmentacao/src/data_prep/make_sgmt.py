import os
import argparse
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from dateutils import relativedelta
from olistlib.db import utils

# diretórios do projeto
DATA_PREP_DIR = os.path.dirname((os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(DATA_PREP_DIR)))
DATA_DIR = os.path.join(BASE_DIR, 'upload_data', 'data')

# insere as datas de início e fim do período de consulta da query sql
parser = argparse.ArgumentParser()
parser.add_argument(
    '--date_end', '-e',
    help='Data de fim da extração',
    default='2018-06-01'
)
args = parser.parse_args()
date_end = args.date_end
date_init = datetime.strptime(date_end, '%Y-%m-%d') - relativedelta(years=1)
date_init = date_init.strftime('%Y-%m-%d')

# importa a query sql
sql_query = utils.import_query(os.path.join(DATA_PREP_DIR, 'segmentos.sql'))
sql_query = sql_query.format(date_init=date_init, date_end=date_end)
create_sql_query = f'''CREATE TABLE tb_seller_sgmt AS {sql_query};'''

insert_sql_query = f'''
    DELETE FROM tb_seller_sgmt WHERE dt_sgmt = '{date_end}';
    INSERT INTO tb_seller_sgmt {sql_query};
'''

# abrir conexão com o banco de dados sqlite
conn = utils.connect_db(db_dir=DATA_DIR)

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

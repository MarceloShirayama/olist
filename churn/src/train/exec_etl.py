import os
import argparse
import pandas as pd
from dateutils import relativedelta
from datetime import datetime
from olistlib.db import utils

TRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(TRAIN_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)
CHURN_DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_BASE_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(OUT_BASE_DIR, "upload_data", "data")

parser = argparse.ArgumentParser()
parser.add_argument(
    "--date_init", "-i", help="Data refêrencia para início da ABT"
)
parser.add_argument(
    "--date_end", "-e", help="Data refêrencia para término da ABT"
)
parser.add_argument(
    "--save_db", "-db", help="Deseja salvar no banco de dados?",
    action="store_true"
)
parser.add_argument(
    "--save_file", "-f", help="Deseja salvar em um arquivo?",
    action="store_true"
)
args = parser.parse_args()
date_init = datetime.strptime(args.date_init, "%Y-%m-%d")
date_end = datetime.strptime(args.date_end, "%Y-%m-%d")
dates = []
while date_init <= date_end:
    dates.append(date_init.strftime("%Y-%m-%d"))
    date_init += relativedelta(months=1)

print('Abrindo conexão com o banco de dados...')
conn = utils.connect_db(db_dir=DATA_DIR)

print('Executando a extração dos dados...')
dfs = []
query_etl_base_path = os.path.join(TRAIN_DIR, "etl_abt_churn.sql")
query_etl_base = utils.import_query(query_etl_base_path)
query_abt_base_path = os.path.join(TRAIN_DIR, "make_abt.sql")
query_abt_base = utils.import_query(query_abt_base_path)
for date in dates:
    query_etl_base = query_etl_base.format(date=date, stage="train")
    query_abt_base = query_abt_base.format(date=date)
    utils.execute_many_sql_query(query_etl_base, conn)
    dfs.append(pd.read_sql_query(query_abt_base, conn))

df = pd.concat(dfs, axis=0, ignore_index=True)

if args.save_db:
    date_init = args.date_init.replace('-', '_')
    date_end = args.date_end.replace('-', '_')
    table_name = 'tb_abt_churn_{date_init}_a_{date_end}'.format(
        date_init=date_init, date_end=date_end
    )
    print(f'Salvando {table_name} no banco de dados')
    df.to_sql(table_name, conn, index=False, if_exists='replace')
    print('Tabela salva com sucesso!')

if args.save_file:
    table_name = 'tb_abt_churn_{date_init}_{date_end}.csv'.format(
        date_init=args.date_init, date_end=args.date_end
    )
    print(f'Salvando em {os.path.join(CHURN_DATA_DIR, table_name)}')
    df.to_csv(os.path.join(CHURN_DATA_DIR, table_name), index=False)
    print('Arquivo salvo com sucesso!')

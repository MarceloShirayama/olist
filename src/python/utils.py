import os
from tqdm import tqdm
import sqlalchemy

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'olist.db')


def import_query(path, **kwargs):
    '''This function performs the import of a query that can receive arguments for the same'''
    with open(path, 'r', **kwargs) as file_query:
        query = file_query.read()
    return query


def connect_db():
    '''Function that provides connection to the database'''
    db_name = os.path.join(DATA_DIR, 'olist')
    str_connection = f'sqlite:///{db_name}.db'
    connection = sqlalchemy.create_engine(str_connection)
    return connection


def execute_many_sql_query(sql_query, conn, verbose=False):
    if verbose:
        for q in tqdm(sql_query.split(';')[:-1]):
            conn.execute(q)
    else:
        for q in sql_query.split(';')[:-1]:
            conn.execute(q)

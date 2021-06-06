import os
import dotenv
from tqdm import tqdm
import sqlalchemy


def import_query(path, **kwargs):
    '''This function performs the import of a query that
    can receive arguments for the same
    '''
    with open(path, 'r', **kwargs) as file_query:
        query = file_query.read()
    return query


def connect_db(db_manager='sqlite', db_dir=None):
    '''Function that provides connection to the database'''
    dotenv.load_dotenv(dotenv.find_dotenv())
    db_name = os.getenv('DATABASE_NAME')
    if db_manager == 'sqlite':
        db_dir = os.path.join(db_dir, db_name)
        str_connection = f'sqlite:///{db_dir}.db'
        connection = sqlalchemy.create_engine(str_connection)
        return connection

    elif db_manager == 'mysql':
        user = os.getenv('DB_USER')
        pwd = os.getenv('DB_PASSWORD')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        str_connection = \
            f'mysql+pymysql://{user}:{pwd}@{host}:{port}/{db_name}'
        return sqlalchemy.create_engine(str_connection)

    elif db_manager == 'postgres':
        user = os.getenv('DB_USER')
        pwd = os.getenv('DB_PASSWORD')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        str_connection = f'postgres://{user}:{pwd}@{host}:{port}/{db_name}'
        return sqlalchemy.create_engine(str_connection)

    else:
        print('Database not found')


def execute_many_sql_query(sql_query, conn, verbose=False):
    if verbose:
        for q in tqdm(sql_query.split(';')[:-1]):
            conn.execute(q)
    else:
        for q in sql_query.split(';')[:-1]:
            conn.execute(q)

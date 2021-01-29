from connection import connect
from create_query_sql import creation_query_list


def create_db(db_name):
    data = {
        'user': 'postgres',
        'password': 'coderslab',
        'port': 5432,
        'host': 'localhost',
        'dbname': 'postgres'
    }
    create_db_query = f"CREATE DATABASE {db_name};"

    conn = connect(data)
    cursor = conn.cursor()

    try:
        cursor.execute(create_db_query)
    except:
        print(f"Baza danych {db_name} już istnieje")

    conn.close()

def create_table(query_list=None):
    if query_list is None:
        query_list = creation_query_list
    conn = connect()
    cursor = conn.cursor()
    for query in query_list:
        try:
            cursor.execute(query)
        except:
            table = query.split('\n')[1][:-1]
            print(f"Nie udało się wykonać zapytania {table}")
    conn.close()

if __name__=='__main__':
    create_db('warsztat_db')
    create_table()


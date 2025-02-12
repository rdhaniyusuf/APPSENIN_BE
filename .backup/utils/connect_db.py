import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

def connect_db():
    try:

        db_name = os.getenv('APPSENIN_DB_NAME')
        db_user = os.getenv('APPSENIN_DB_USER')
        db_password = os.getenv('APPSENIN_DB_PASSWORD')
        db_host = os.getenv('APPSENIN_DB_HOST')
        db_port = os.getenv('APPSENIN_DB_PORT')

        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )

        print("Database connection successful")
        return connection

    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None
    
def close_db(connection):
    connection.close()
    print("Database connection closed")
    
def query_db(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data is None:
            cursor.execute(query)
        else:
            cursor.execute(query, data)
        connection.commit()
        return cursor
    except Exception as error:
        print(f"Error querying database: {error}")
        return None
    finally:
        cursor.close()

def fetch_all(cursor):
    return cursor.fetchall()
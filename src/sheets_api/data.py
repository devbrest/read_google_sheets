#!/usr/bin/python

import psycopg2
from config import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        #print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        #print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return conn
            #print('Database connection closed.')

def create_database():
    """Create PostgreSQL database"""
    conn = None
    try:
        params = config()
        newDatabase = params['database']
        params['database'] = "postgres"
        conn = psycopg2.connect(**params)
        
        conn.autocommit = True

        cursor = conn.cursor()

        sql = f"""CREATE database {newDatabase}""";

        #Creating a database
        cursor.execute(sql)
        print("Database created successfully........")
        params = config()
        conn = psycopg2.connect(**params)
        createTableQuery = """CREATE TABLE IF NOT EXISTS my_orders(
        id BIGSERIAL PRIMARY KEY NOT NULL, 
        my_order varchar, 
        my_amount numeric(15,2), 
        my_date TIMESTAMP NOT NULL DEFAULT current_timestamp,
        my_rub_amount numeric(15,2));  """
        cursor.execute(createTableQuery)
        # close the communication with the PostgreSQL
        cursor.close()
        #Closing the connection
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

def select(sqlQuery, conn) -> list:
    try:
        cursor = conn.cursor()
        cursor.execute(sqlQuery)
        all_records = cursor.fetchall()
        # close the communication with the PostgreSQL
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return all_records

def run_query(sqlQuery, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(sqlQuery)
        # close the communication with the PostgreSQL
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


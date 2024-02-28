#! python
# connect to postgres database

import os
import logging


import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv #for loading environment variables


logging.basicConfig(filename='log.log', 
                    filemode='w', 
                    encoding='utf-8', 
                    format='%(asctime)s | %(levelname)s: %(message)s',
                    level=logging.INFO
                    )



# loads environment variables using absolute filepath and assign
load_dotenv(os.path.join(os.getcwd(),".env.txt"))

# assign environment variables
DB_CONFIG = {'user':os.environ.get("DB_USERNAME"),
             'password':os.environ.get("DB_PASSWORD"),
             'host':os.environ.get("DB_HOSTNAME"),
             'port':os.environ.get("DB_PORT"),
             'database':os.environ.get("DB_NAME")}


def database_import(file):
    """
    Connect to database and copy data from file to database table.

    Arg:
        file: File containing data to copy to database.
    """

    # wrapped in try-catch to return errors or close successful connection
    try:
        # connect to database using environment variables
        conn = psycopg2.connect(**DB_CONFIG)

        logging.info('Database connection established.')

        # connection context manager commits/closes transaction    
        with conn:
            # cursor context manager to scope session        
            with conn.cursor() as cur:
                # delete existing data from game_data table before update
                cur.execute("DELETE FROM game_data;")

                # copy file data to database, assign NA values as NULL in table
                with open(file, encoding='utf-8') as csv_fo:                    
                    cur.copy_expert("""
                                    COPY game_data 
                                    FROM STDIN
                                    WITH CSV HEADER 
                                    DELIMITER ','
                                    NULL 'NA';
                                    """, 
                                    csv_fo
                                    )
                # query table row count
                cur.execute("""
                            SELECT COUNT(*) 
                            FROM game_data;
                            """)
                
                # return row count query result
                row_count = cur.fetchone()
                
                logging.info(f'Records copied: {row_count}')

    except (Exception, Error) as error:
        logging.error('PostgreSQL Connection Error', error)

    finally:
        # if connection still open, close connection
        if (conn):        
            conn.close()
            logging.info('PostgreSQL connection closed.')



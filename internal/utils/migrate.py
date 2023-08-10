import mysql.connector
import os
import logging


DIRECTORY = "./database/migrations"


def migrate(connection: mysql.connector.connection.MySQLCursor):
    """migrate database sql files

    :param connection: mysql connection cursor
    """
    for file in [filename for filename in os.listdir(DIRECTORY) if filename.startswith('up')]:
        with open(DIRECTORY+"/"+file, 'r') as f:
            query = f.read()
            connection.execute(query)

            logging.info(f"migrated: {file}")

    connection.close()

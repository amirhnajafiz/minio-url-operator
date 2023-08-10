import mysql.connector
import os
import logging


DIRECTORY = "./database/migrations"


def migrate(connection: mysql.connector.connection.MySQLConnection) -> bool:
    """migrate database sql files

    :param connection: mysql connection
    :return: bool, for result
    """
    if not connection.is_connected():
        return False

    cursor = connection.cursor()

    for file in [filename for filename in os.listdir(DIRECTORY) if filename.startswith('up')]:
        with open(DIRECTORY+"/"+file, 'r') as f:
            query = f.read()
            cursor.execute(query)

            logging.info(f"migrated: {file}")

    cursor.close()

    return True

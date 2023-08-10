import mysql.connector


class MySQL(object):
    """MySQL manages the connection to database"""

    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        # opening a connection to mysql server
        self.connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

    def ping(self) -> bool:
        """return a boolean to check database connection"""
        return self.connection.is_connected()

    def get_cursor(self) -> mysql.connector.connection.MySQLCursor:
        """returns a cursor of connection"""
        return self.connection.cursor()

    def commit(self):
        """commit updates on connection"""
        self.connection.commit()

    def close_connection(self):
        """closes the database connection"""
        self.connection.close()

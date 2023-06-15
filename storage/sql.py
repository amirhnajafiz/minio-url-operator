import sqlite3
import os


class SQLConnector(object):
    """SQLConnector manages the connection to database"""

    def __init__(self, host: str):
        self._create_host(host)
        self.connection = sqlite3.connect(host, check_same_thread=False)

    def get_cursor(self) -> sqlite3.Cursor:
        """returns a cursor of connection"""
        return self.connection.cursor()

    def close_connection(self):
        """closes the database connection"""
        self.connection.close()

    @staticmethod
    def _close_cursor(cursor: sqlite3.Cursor):
        """closes cursor

        :param cursor: db cursor
        """
        cursor.close()

    @staticmethod
    def _create_host(host: str):
        """create database host

        :param host: host address
        """
        if not os.path.exists(host):
            f = open(host, "a")
            f.close()

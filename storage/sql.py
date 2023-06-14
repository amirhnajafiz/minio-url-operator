import sqlite3
import os


class SQLConnector(object):
    def __int__(self, host):
        self._create_host(host)
        self.connection = sqlite3.connect(host, check_same_thread=False)

    def get_cursor(self):
        return self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    @staticmethod
    def _close_cursor(cursor: sqlite3.Cursor):
        cursor.close()

    @staticmethod
    def _create_host(host):
        if not os.path.exists(host):
            f = open(host, "a")
            f.close()

import sqlite3
import minio


class Handler(object):
    """Handler manages the logic of our backend"""

    def __init__(self, database: sqlite3.Connection, minio_connection: minio.Minio):
        self.database = database
        self.minio_connection = minio_connection

    def get_objects(self):
        pass

    def get_object_url(self):
        pass

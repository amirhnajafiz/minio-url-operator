from storage.sql import SQLConnector
from storage.minio import MinioConnector


class Handler(object):
    """Handler manages the logic of our backend"""

    def __init__(self, database: SQLConnector, minio_connection: MinioConnector):
        self.database = database
        self.minio_connection = minio_connection

    def get_objects(self):
        pass

    def get_object_url(self):
        pass

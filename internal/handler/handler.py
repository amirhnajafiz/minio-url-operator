from datetime import datetime

from storage.sql import SQLConnector
from storage.minio import MinioConnector
from model.url import URL


class Handler(object):
    """Handler manages the logic of our backend"""

    def __init__(self, database: SQLConnector, minio_connection: MinioConnector):
        self.database = database
        self.minio_connection = minio_connection

    def get_objects(self, bucket, prefix=""):
        """get objects of a bucket based on prefix

        :param bucket: minio bucket
        :param prefix: objects prefix
        :return: list of objects metadata
        """
        client = self.minio_connection.get_connection()

        return client.list_objects(bucket, prefix=prefix)

    def get_object_url(self, bucket: str, key: str) -> str:
        """get selected object url

        :param bucket: object minio bucket
        :param key: object key
        :return: object url
        """
        # get a new cursor
        cursor = self.database.get_cursor()

        # select a url from database
        cursor.execute(f'SELECT * FROM object_urls WHERE bucket = ? AND object = ?', [bucket, key])

        # fetch the first item
        record = cursor.fetchone()

        # create the url
        url = URL()
        url.read(record)

        t1 = datetime.fromtimestamp(url.createdAt)
        t2 = datetime.now()

        if ((t2 - t1).total_seconds() / 3600 * 24 * 6) < 7:
            client = self.minio_connection.get_connection()
            address = client.presigned_get_object(
                bucket, key, expires=7,
            )

            url.url = address

        # todo: [1] if not exists create one
        # todo: [2] if exists check the url time past 7 days
        # todo: [3] if 1 or 2 create a new link
        # todo: [4] return the link

        return ""

from datetime import datetime

from storage.sql import SQLConnector
from storage.minio import MinioConnector
from model.url import URL


class Handler(object):
    """Handler manages the logic of our backend"""

    def __init__(self, database: SQLConnector, minio_connection: MinioConnector):
        self.database = database
        self.minio_connection = minio_connection
        self.time_factor = 3600 * 24 * 6
        self.time_limit = 7

    def get_objects_metadata(self, bucket, prefix=""):
        """get objects of a bucket based on prefix

        :param bucket: minio bucket
        :param prefix: objects prefix
        :return: list of objects metadata
        """
        client = self.minio_connection.get_connection()

        return client.list_objects(bucket, prefix=prefix)

    def get_object(self, bucket: str, key: str) -> (URL, bool):
        """get object from database

        :param bucket: object bucket
        :param key: object key
        :return: URL if exists, None if not exists
        """
        # get a new cursor
        cursor = self.database.get_cursor()

        # select a url from database
        cursor.execute(f'SELECT * FROM object_urls WHERE bucket = ? AND object = ?', [bucket, key])

        # fetch the first item
        record = cursor.fetchone()
        if record is None:
            return URL(), False

        # create the url
        url = URL()
        url.read(record)

        return url, True

    def check_url_time(self, url: URL) -> bool:
        """check if the url is expired or not

        :param url: input url object
        :return: true or false
        """
        t1 = datetime.fromtimestamp(url.createdAt)
        t2 = datetime.now()

        return ((t2 - t1).total_seconds() / self.time_factor) < self.time_limit

    def create_url_for_object(self, bucket: str, key: str) -> str:
        """create url for object in minio

        :param bucket: object bucket
        :param key: object name
        :return: url of object
        """
        client = self.minio_connection.get_connection()

        return client.presigned_get_object(
            bucket, key, expires=self.time_limit,
        )

    def get_object_url(self, bucket: str, key: str) -> str:
        """get selected object url

        :param bucket: object minio bucket
        :param key: object key
        :return: object url
        """

        # todo: [1] if not exists create one
        # todo: [2] if exists check the url time past 7 days
        # todo: [3] if 1 or 2 create a new link
        # todo: [4] return the link

        return ""

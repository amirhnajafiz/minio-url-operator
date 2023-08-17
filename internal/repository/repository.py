from datetime import datetime, timedelta

from utils import get_random_string

from ..storage.minio import MinioConnector
from ..storage.mysql import MySQL

from database.model.url import URL


class Repository(object):
    def __init__(self, database: MySQL, minio_connection: MinioConnector):
        self.database = database
        self.minio_connection = minio_connection

    def __create_url_for_object__(self, bucket: str, key: str, limit: int) -> str:
        """create url for object in minio

        :param bucket: object bucket
        :param key: object name
        :return: url of object
        """
        client = self.minio_connection.get_connection()

        return client.presigned_get_object(
            bucket, key, expires=timedelta(days=limit),
        )

    def __create_object__(self, url: URL):
        """create a new object in database

        :param url: url object
        """
        # get a new cursor
        cursor = self.database.get_cursor()

        cursor.execute(
            "INSERT INTO `urls` (bucket, object_key, url, created_at, address, status) VALUES (%s,%s,%s,%s,%s,%s);",
            url.write()
        )

        self.database.commit()

        cursor.close()

    def register_object(self, bucket: str, key: str, limit: int):
        """register an object into our system

        :param bucket: bucket name
        :param key: object key
        :param limit: days of expiration
        """
        address = get_random_string(10)
        url = URL(bucket, key, self.__create_url_for_object__(bucket, key, limit), address)
        url.createdAt = datetime.now()

        self.__create_object__(url)

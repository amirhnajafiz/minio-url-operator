from datetime import datetime, timedelta
import random
import string

from ...storage.minio import MinioConnector
from ...storage.mysql import MySQL
from database.model.url import URL


def get_random_string(length: int) -> str:
    """generate a random string for address

    :param length: size of string
    :return: random string
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


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

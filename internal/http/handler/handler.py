from datetime import datetime, timedelta
import random
import string

from ...storage.mysql import MySQL
from ...storage.minio import MinioConnector
from database.model.url import URL


def get_random_string(length: int) -> str:
    """generate a random string for address

    :param length: size of string
    :return: random string
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


class Handler(object):
    """Handler manages the logic of our backend"""

    def __init__(self, database: MySQL, minio_connection: MinioConnector):
        self.database = database
        self.minio_connection = minio_connection
        self.time_factor = 3600 * 24 * 6
        self.time_limit = 7

    def get_objects_metadata(self, bucket, prefix="") -> list:
        """get objects of a bucket based on prefix

        :param bucket: minio bucket
        :param prefix: objects prefix
        :return: list of objects metadata
        """
        client = self.minio_connection.get_connection()

        objects = client.list_objects(bucket, prefix=prefix)

        objects_list = []

        for item in objects:
            tmp, valid = self.__get_object__(bucket, item.object_name)
            if not valid:
                object_pack = {
                    'name': item.object_name,
                    'status': -1,
                }
            else:
                object_pack = {
                    'name': item.object_name,
                    'status': tmp.status,
                    'created_at': tmp.createdAt
                }

            objects_list.append(object_pack)

        return objects_list

    def __get_object__(self, bucket: str, key: str) -> (URL, bool):
        """get object from database

        :param bucket: object bucket
        :param key: object key
        :return: URL if exists, None if not exists
        """
        # get a new cursor
        cursor = self.database.get_cursor()

        # select a url from database
        cursor.execute(f'SELECT * FROM `urls` WHERE `bucket` = %s AND `object_key` = %s', [bucket, key])

        # fetch the first item
        record = cursor.fetchone()
        if record is None:
            return URL(), False

        # create the url
        url = URL()
        url.read(record)

        cursor.close()

        return url, True

    def __check_url_time__(self, url: URL) -> bool:
        """check if the url is expired or not

        :param url: input url object
        :return: true or false
        """
        t1 = datetime.strptime(url.createdAt, "%Y-%m-%d %H:%M:%S.%f").date()
        t2 = datetime.now().date()

        return ((t2 - t1).total_seconds() / self.time_factor) < self.time_limit

    def __create_url_for_object__(self, bucket: str, key: str) -> str:
        """create url for object in minio

        :param bucket: object bucket
        :param key: object name
        :return: url of object
        """
        client = self.minio_connection.get_connection()

        return client.presigned_get_object(
            bucket, key, expires=timedelta(days=self.time_limit),
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

    def __update_object_url__(self, url: URL):
        """update url for an object

        :param url: url object
        """
        # get a new cursor
        cursor = self.database.get_cursor()

        cursor.execute("UPDATE `urls` SET `url` = %s, `created_at` = %s WHERE `id` = %s", [url.url, url.createdAt, url.id])

        self.database.commit()

        cursor.close()

    def __get_object_url(self, bucket: str, key: str) -> str:
        """get selected object url

        :param bucket: object minio bucket
        :param key: object key
        :return: object url
        """
        # get object from database
        url, valid = self.__get_object__(bucket, key)

        # if not valid then create url and save it into database
        if not valid:  # create a new instance
            address = get_random_string(10)
            url = URL(bucket, key, self.__create_url_for_object__(bucket, key), address)
            url.createdAt = datetime.now()

            self.__create_object__(url)
        elif not self.__check_url_time__(url):  # if it was expired create new one
            url.url = self.__create_url_for_object__(url.bucket, url.key)
            url.createdAt = datetime.now()

            self.__update_object_url__(url)

        return url.url

    def update_object(self, bucket: str, key: str, status: int):
        """update url status to set enable value

        :param bucket: object bucket
        :param key: object key
        :param status: object status
        """
        # get a new cursor
        cursor = self.database.get_cursor()

        cursor.execute("UPDATE `urls` SET `status` = %s WHERE `bucket` = %s AND `object_key` = %s", [status, bucket, key])
        self.database.commit()

        cursor.close()

    def get_object_address(self, bucket: str, key: str) -> str:
        """get address of an object

        :param bucket: object bucket
        :param key: object key
        :return: address
        """
        # get a new cursor
        cursor = self.database.get_cursor()

        cursor.execute("SELECT `address` FROM `urls` WHERE `bucket` = %s AND `object_key` = %s", [bucket, key])

        url = cursor.fetchone()

        cursor.close()

        return url[0]

    def register_object(self, bucket, key) -> str:
        """register an object into our system

        :param bucket: bucket name
        :param key: object key
        """
        return self.__get_object_url(bucket, key)

    def get_object_url_by_address(self, address: str) -> str:
        """get object url by its address

        :param address: object address
        :return: url of that object
        """
        # get a new cursor
        cursor = self.database.get_cursor()

        cursor.execute("SELECT * FROM `urls` WHERE `address` = %s", [address])

        row = cursor.fetchone()
        if row is None:
            return ""

        url = URL()
        url.read(row)

        if url.status == 1:
            return ""

        cursor.close()

        return self.__get_object_url(url.bucket, url.key)

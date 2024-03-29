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
            tmp = self.__get_object__(bucket, item.object_name)

            object_pack = {
                'name': item.object_name,
                'address': tmp.address,
                'status': tmp.status,
                'created_at': tmp.createdAt,
                'updated_at': tmp.updatedAt,
                'expires_at': tmp.expiresAt
            }

            objects_list.append(object_pack)

        return objects_list

    def __get_object__(self, bucket: str, key: str) -> URL:
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
        if record is None:  # if not found then we register it
            self.__register_object(bucket, key)

            # now we read it again
            cursor.execute(f'SELECT * FROM `urls` WHERE `bucket` = %s AND `object_key` = %s', [bucket, key])
            record = cursor.fetchone()

        # create the url
        url = URL()
        url.read(record)

        cursor.close()

        return url

    def __check_url_time__(self, url: URL) -> bool:
        """check if the url is expired or not

        :param url: input url object
        :return: true or false
        """
        t1 = url.createdAt.date()
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
            '''INSERT INTO `urls` (bucket, object_key, url, created_at, address, status, expires_at, updated_at) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s);''',
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

        cursor.execute(
            '''UPDATE `urls` SET `url` = %s, `created_at` = %s WHERE `id` = %s''',
            [url.url, url.createdAt, url.id]
        )

        self.database.commit()

        cursor.close()

    def update_object(self, bucket: str, key: str, status: int, expires: datetime):
        """update url status to set enable value

        :param bucket: object bucket
        :param key: object key
        :param status: object status
        :param expires: expire time
        """
        # get a new cursor
        cursor = self.database.get_cursor()

        cursor.execute(
            '''UPDATE `urls` 
                SET `status` = %s, `expires_at` = %s, `updated_at` = %s 
                WHERE `bucket` = %s AND `object_key` = %s''',
            [status, expires, datetime.now(), bucket, key]
        )
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

    def __register_object(self, bucket, key):
        """register an object into our system

        :param bucket: bucket name
        :param key: object key
        """
        address = get_random_string(10)
        url = URL(bucket, key, self.__create_url_for_object__(bucket, key), address)
        url.createdAt = datetime.now()

        self.__create_object__(url)

    def get_object_url_by_address(self, address: str) -> str:
        """get object url by its address

        :param address: object address
        :return: url of that object
        """
        # get a new cursor
        cursor = self.database.get_cursor()

        cursor.execute(
            '''SELECT * FROM `urls` 
                WHERE `address` = %s AND `status` = 1 AND `expires_at` > NOW()''',
            [address]
        )

        row = cursor.fetchone()
        if row is None:
            return ""

        url = URL()
        url.read(row)

        cursor.close()

        url = self.__get_object__(url.bucket, url.key)

        if not self.__check_url_time__(url):  # if it was expired create new one
            url.url = self.__create_url_for_object__(url.bucket, url.key)
            url.createdAt = datetime.now()

            self.__update_object_url__(url)

        return url.url

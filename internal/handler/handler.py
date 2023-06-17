from storage.sql import SQLConnector
from storage.minio import MinioConnector


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

        # todo: [1] if not exists create one
        # todo: [2] if exists check the url time past 7 days
        # todo: [3] if 1 or 2 create a new link
        # todo: [4] return the link

        # url = client.presigned_get_object(
        #     "my-bucket", "my-object", expires=timedelta(hours=2),
        # )

        return ""

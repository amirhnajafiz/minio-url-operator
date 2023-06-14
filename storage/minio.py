import minio
from minio import Minio


class MinioConnector(object):
    """MinioConnector is used to connect to Minio cluster"""

    def __init__(self, host: str, access: str, secret: str):
        self.conn = Minio(
            host,
            access_key=access,
            secret_key=secret,
        )

    def get_connection(self) -> minio.Minio:
        """get minio connection

        :return: minio connection
        """
        return self.conn

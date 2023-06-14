import minio
from minio import Minio


class MinioConnector(object):
    def __init__(self, host, access, secret):
        self.conn = Minio(
            host,
            access_key=access,
            secret_key=secret,
        )

    def get_connection(self) -> minio.Minio:
        return self.conn

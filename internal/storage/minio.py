from minio import Minio


class MinioConnector(object):
    """MinioConnector is used to connect to Minio cluster"""

    def __init__(self, host: str, access: str, secret: str, secure: bool):
        self.conn = Minio(
            host,
            access_key=access,
            secret_key=secret,
            secure=secure,
        )

    def ping(self) -> (str, bool):
        """ping minio cluster

        :return: (error message, error flag)
        """
        try:
            self.conn.bucket_exists("test_bucket")
        except Exception as e:
            return f"[minioConnector.ping]' failed to connect to minio cluster error={e}", True

        return "OK", False

    def get_connection(self) -> Minio:
        """get minio connection

        :return: minio connection
        """
        return self.conn

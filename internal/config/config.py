from .env import read_value_from_env


class Config(object):
    """Config object is used to store config variables of application"""

    def __init__(self):
        self.host = None
        self.private = False
        self.port = None
        self.debug = True

        self.minio = {}
        self.mysql = {}

    def load(self) -> (str, bool):
        """"load configs into class fields

        :returns: (error type, error flag)
        """
        try:
            self.host = read_value_from_env("HTTP_HOST")

            self.private = read_value_from_env("HTTP_PRIVATE")
            self.private = True if self.private == "true" else False

            self.port = int(read_value_from_env("HTTP_PORT"))

            self.debug = read_value_from_env("HTTP_DEBUG")
            self.debug = True if self.debug == "true" else False

            self.mysql['host'] = read_value_from_env("MYSQL_HOST")
            self.mysql['port'] = int(read_value_from_env("MYSQL_PORT"))
            self.mysql['user'] = read_value_from_env("MYSQL_USER")
            self.mysql['pass'] = read_value_from_env("MYSQL_PASSWORD")
            self.mysql['name'] = read_value_from_env("MYSQL_DB")

            self.mysql['migrate'] = read_value_from_env("MYSQL_MIGRATE")
            self.mysql['migrate'] = True if self.mysql['migrate'] == "true" else False

            self.minio['host'] = read_value_from_env("MINIO_HOST")
            self.minio['access'] = read_value_from_env("MINIO_ACCESS")
            self.minio['secret'] = read_value_from_env("MINIO_SECRET")

            self.minio['secure'] = read_value_from_env("MINIO_SECURE")
            self.minio['secure'] = True if self.minio['secure'] == "true" else False

        except Exception as e:
            return f"[config.load] failed to read params error={e}", True

        return "OK", False

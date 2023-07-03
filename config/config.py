from .env import read_value_from_env


class Config(object):
    """Config object is used to store config variables of application"""

    def __init__(self):
        self.host = None
        self.private = False
        self.port = None
        self.debug = True

        self.minio = {}
        self.sql = {
            'host': 'database/sql.db'
        }

    def load(self) -> (str, bool):
        """"load configs into class fields

        :returns: (error type, error flag)
        """
        try:
            self.host = read_value_from_env("HTTP_HOST")
            self.private = int(read_value_from_env("HTTP_PRIVATE"))
            self.private = True if self.private == 0 else False
            self.port = int(read_value_from_env("HTTP_PORT"))
            self.debug = int(read_value_from_env("HTTP_DEBUG"))
            self.debug = True if self.debug == 0 else False

            self.minio['host'] = read_value_from_env("MINIO_HOST")
            self.minio['access'] = read_value_from_env("MINIO_ACCESS")
            self.minio['secret'] = read_value_from_env("MINIO_SECRET")
            self.minio['secure'] = int(read_value_from_env("MINIO_SECURE"))
            self.minio['secure'] = True if self.minio['secure'] == 0 else False

        except Exception as e:
            return f"[config.load] failed to read params error={e}", True

        return "OK", False

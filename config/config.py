from .env import read_value_from_env


class Config(object):
    """Config object is used to store config variables of application"""

    def __init__(self):
        self.port = None
        self.debug = True

        self.minio = {}
        self.sql = {}

    def load(self) -> (str, bool):
        """"load configs into class fields

        :returns: (error type, error flag)
        """
        try:
            self.port = int(read_value_from_env("HTTP_PORT"))
            self.debug = bool(read_value_from_env("HTTP_DEBUG"))

            self.minio['host'] = read_value_from_env("MINIO_HOST")
            self.minio['access'] = read_value_from_env("MINIO_ACCESS")
            self.minio['secret'] = read_value_from_env("MINIO_SECRET")

            self.sql['host'] = read_value_from_env("SQL_HOST")
        except Exception as e:
            return f"[config.load] failed to read params error={e}", True

        return "OK", False

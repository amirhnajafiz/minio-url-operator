from env import read_value_from_env


class Config(object):
    """Config object is used to store config variables of application"""
    def __int__(self):
        self.port = read_value_from_env("HTTP_PORT")

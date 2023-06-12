from .env import read_value_from_env


class Config(object):
    """Config object is used to store config variables of application"""

    def __init__(self):
        self.port = None
        self.debug = True

    def load(self):
        """"load configs into class fields"""
        self.port = int(read_value_from_env("HTTP_PORT"))
        self.debug = bool(read_value_from_env("HTTP_DEBUG"))

import os


def read_value_from_env(key: str) -> str:
    """Read environment variable.

    :param key: name of the variable
    :return: value of the variable
    """
    return os.getenv(key)

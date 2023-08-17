import random
import string


def get_random_string(length: int) -> str:
    """generate a random string for address

    :param length: size of string
    :return: random string
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

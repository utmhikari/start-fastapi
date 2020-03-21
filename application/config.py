import os
from typing import Any


def get(key: str, default: Any = '') -> Any:
    """
    get one config value
    :param key: config key
    :param default: default value
    :return: config value
    """
    return os.getenv(key.upper(), default)


def get_bool(key: str) -> bool:
    """
    get bool config value
    :param key: config key
    :return: bool config
    """
    return str(os.getenv(key.upper())).upper() == 'TRUE'

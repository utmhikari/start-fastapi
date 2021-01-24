import os
import sys
from typing import Any


def get(key: str, default: Any = '') -> Any:
    """
    get one config value
    :param key: config key
    :param default: default value
    :return: config value
    """
    return os.getenv(key.upper(), default)


def get_str(key: str) -> str:
    """
    get string config value
    :param key: config key
    :return: string config value
    """
    return str(get(key))


def get_bool(key: str) -> bool:
    """
    get bool config value
    :param key: config key
    :return: bool config value
    """
    return str(get(key)).upper() == 'TRUE'


def get_int(key: str, panic: bool = True) -> int:
    """
    get int config value
    :param key: config key
    :param panic: will raise exception if fail
    :return: int config vallue
    """
    try:
        return int(str(get(key)))
    except Exception as e:
        if panic:
            raise e
        print('[core.lib.cfg] get int value of key %s error' % key, file=sys.stderr)
        return 0


def get_float(key: str, panic: bool = True) -> float:
    """
    get float config  value
    :param key: config key
    :param panic: will raise exception if fail
    :return: float config value
    """
    try:
        return float(str(get(key)))
    except Exception as e:
        if panic:
            raise e
        print('[core.lib.cfg] get float value of key %s error' % key, file=sys.stderr)
        return 0.0

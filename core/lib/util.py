"""
Common/Misc utils
"""

import platform
import pprint
import typing
from typing import Any, Tuple, Optional

T = typing.TypeVar('T')


# global encoding
ENCODING = 'utf-8'


def as_int(o: Any) -> Tuple[int, Optional[Exception]]:
    """
    object to int
    :param o: object
    :return: int value, err
    """
    try:
        return int(o), None
    except Exception as e:
        return 0, e


def as_float(o: Any) -> Tuple[float, Optional[Exception]]:
    """
    object to float
    :param o: object
    :return: float value, err
    """
    try:
        return float(o), None
    except Exception as e:
        return 0.0, e


def is_win() -> bool:
    """
    is currently running on windows
    :return: if current system is of Windows family
    """
    return platform.system().lower().startswith('win')


def pfmt(o: Any, *args, **kwargs) -> str:
    """
    pretty format object
    :param o: object
    :return: object string
    """
    return pprint.pformat(o, *args, **kwargs)

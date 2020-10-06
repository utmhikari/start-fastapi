"""
Common Utils
"""

from typing import Any
import pprint
import hashlib
import json


def jsondump(o: Any, **kwargs) -> str:
    """
    json dump object
    :return:
    """
    return json.dumps(o, indent=2, ensure_ascii=False, **kwargs)


def md5hash(s: str, length: int = 16) -> str:
    """
    md5 hash
    :param s: string
    :param length: length (default is 8)
    :return: hashed string
    """
    if length <= 0 or length > 32:
        length = 16
    ret = hashlib.md5(s.encode()).hexdigest()
    if len(ret) > length:
        ret = ret[:length]
    return ret


def pfmt(o: Any) -> str:
    """
    pretty format object
    :param o: object
    :return: object string
    """
    return pprint.pformat(o, indent=2, width=60)

from typing import Any, Dict
import logging


def get_logger(name):
    """
    get middleware logger
    :param name: middleware name
    :return: middleware logger
    """
    return logging.getLogger('CONTROLLER_' + name)


def success(data: Any = None, msg: str = '') -> Dict[str, Any]:
    """
    generate success response body
    :param data: data
    :param msg: message
    :return: json resp body
    """
    return {
        'data': data,
        'success': True,
        'message': msg,
        'code': 0,
    }


def error(data: Any = None, msg: str = '', code: int = -1) -> Dict[str, Any]:
    """
    generate error response body with external status code 200
    :param data: data
    :param msg: message
    :param code: user defined (not http) status code
    :return: json resp body
    """
    return {
        'data': data,
        'success': False,
        'message': msg,
        'code': code,
    }

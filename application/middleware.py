import logging


def get_logger(name: str):
    """
    get middleware logger
    :param name: middleware name
    :return: middleware logger
    """
    return logging.getLogger('MIDDLEWARE_' + name)

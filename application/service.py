import logging


def get_logger(name: str):
    """
    get service logger
    :param name: service name
    :return: service logger
    """
    return logging.getLogger('SERVICE_' + name)

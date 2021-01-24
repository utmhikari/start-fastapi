import logging


def get(name: str = '', tag: str = '') -> logging.Logger:
    """
    get logger of specific tag
    :param name: name of the logger
    :param tag: tag of the logger
    :return: logger instance
    """
    if tag:
        logger_name = (tag + '_' + name).upper()
    else:
        logger_name = name.upper()
    return logging.getLogger(logger_name)


def for_handler(name: str) -> logging.Logger:
    """
    get handler logger
    :param name: handler name
    :return: controller logger
    """
    return get('handler', name)


def for_middleware(name: str) -> logging.Logger:
    """
    get middleware logger
    :param name: middleware name
    :return: middleware logger
    """
    return get('middleware', name)


def for_model(name: str) -> logging.Logger:
    """
    get model logger
    :param name: model name
    :return: model logger
    """
    return get('model', name)


def for_service(name: str) -> logging.Logger:
    """
    get service logger
    :param name: service name
    :return: service logger
    """
    return get('service', name)

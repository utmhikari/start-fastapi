import logging


def get_application_logger():
    """
    get application logger
    :return:
    """
    return logging.getLogger('APPLICATION')


def get_controller_logger(name):
    """
    get controller logger
    :param name: controller name
    :return: controller logger
    """
    return logging.getLogger('CONTROLLER_' + str(name).upper())


def get_middleware_logger(name: str):
    """
    get middleware logger
    :param name: middleware name
    :return: middleware logger
    """
    return logging.getLogger('MIDDLEWARE_' + str(name).upper())


def get_service_logger(name: str):
    """
    get service logger
    :param name: service name
    :return: service logger
    """
    return logging.getLogger('SERVICE_' + str(name).upper())

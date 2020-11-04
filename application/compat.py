"""
Compatible module
"""
import platform
import asyncio
from application import logger

LOGGER = logger.get_application_logger()


def is_windows() -> bool:
    """
    is currently running on windows
    :return:
    """
    print(platform.system())
    return platform.system().lower().startswith('win')


def set_proactor_eventloop() -> None:
    """
    set eventloop as ProactorEventLoop, used on windows
    :return:
    """
    LOGGER.warning('Set ProactorEventLoop for asyncio...')
    asyncio.set_event_loop(asyncio.ProactorEventLoop())

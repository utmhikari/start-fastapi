"""
Concurrency module
"""
import asyncio
from concurrent.futures import ProcessPoolExecutor
import functools
import typing
from application import logger
import pprint

LOGGER = logger.get_application_logger()

T = typing.TypeVar('T')

PROCESS_POOL_EXECUTOR = ProcessPoolExecutor()


async def run_in_processpool(func: typing.Callable[..., T],
                             *args: typing.Any,
                             **kwargs: typing.Any) -> T:
    """
    run in process pool executor
    :param func: function
    :param args: args
    :param kwargs: keyword args
    :return:
    """
    LOGGER.debug('Run in processpool with func: %s, args: %s, kwargs: %s' %
                 (pprint.pformat(func), pprint.pformat(args), pprint.pformat(kwargs)))
    loop = asyncio.get_event_loop()
    f = functools.partial(func, **kwargs)
    return await loop.run_in_executor(None, f, *args)

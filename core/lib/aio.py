"""
Async IO module
"""
import asyncio
import functools
import typing
from concurrent.futures import ProcessPoolExecutor

T = typing.TypeVar('T')

PROCESS_POOL_EXECUTOR = ProcessPoolExecutor()


async def run_in_processpool(func: typing.Callable[..., T],
                             *args: typing.Any,
                             **kwargs: typing.Any) -> T:
    """
    run task in process pool executor
    :param func: function
    :param args: args
    :param kwargs: keyword args
    :return: result of the function
    """
    loop = asyncio.get_event_loop()
    f = functools.partial(func, **kwargs)
    return await loop.run_in_executor(PROCESS_POOL_EXECUTOR, f, *args)


def set_proactor_eventloop() -> None:
    """
    set eventloop as ProactorEventLoop, maybe used in windows system
    then in uvicorn main script, add these codes:
    >>> from uvicorn.config import LOOP_SETUPS
    >>> LOOP_SETUPS['asyncio'] = 'core.lib.aio:set_proactor_eventloop'
    if proactor loop is set, do not enable reload in
    :return: None
    """
    asyncio.set_event_loop(asyncio.ProactorEventLoop())

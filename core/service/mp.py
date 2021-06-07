import asyncio
import functools
import typing
from concurrent.futures import ProcessPoolExecutor

T = typing.TypeVar('T')

# worker pool starts in main process
_WORKER_POOL: typing.Optional[ProcessPoolExecutor] = None

# task pool launched in workers
_TASK_POOL: typing.Optional[ProcessPoolExecutor] = None


def get_worker_pool() -> ProcessPoolExecutor:
    """
    get worker pool instance
    should be executed in main process
    main process -> worker 1 -> task 1
                                task 2
                                task 3
                    worker 2 -> task 1
                                task 2
                                task 3
                    worker 3 -> task 1
                                task 2
                                task 3
    task pool should be released once tasks are finished
    while worker pool should be always held at background
    :return: worker pool instance
    """
    global _WORKER_POOL
    if not _WORKER_POOL:
        _WORKER_POOL = ProcessPoolExecutor()
    return _WORKER_POOL


def get_task_pool() -> ProcessPoolExecutor:
    """
    get task pool instance
    should be executed in worker logics
    :return: task pool instance
    """
    global _TASK_POOL
    if not _TASK_POOL:
        _TASK_POOL = ProcessPoolExecutor()
    return _TASK_POOL


def release_task_pool():
    """
    release task pool instance to avoid memory leak
    :return: None
    """
    global _TASK_POOL
    if not _TASK_POOL:
        return
    _TASK_POOL.shutdown()
    _TASK_POOL = None


async def run_in_worker(func: typing.Callable[..., T],
                        *args: typing.Any,
                        **kwargs: typing.Any) -> T:
    """
    run single task in worker
    :param func: function
    :param args: args
    :param kwargs: keyword args
    :return: result of the function
    """
    loop = asyncio.get_event_loop()
    f = functools.partial(func, **kwargs)
    worker_pool = get_worker_pool()
    return await loop.run_in_executor(worker_pool, f, *args)

import datetime

from starlette.requests import Request
from starlette.responses import StreamingResponse

from core.lib import logger

LOGGER = logger.for_middleware('test')


async def calc_time(request: Request, next_func):
    """
    an example of calculating time
    CAUTION: this middleware may block the main loop, do not use for async def handlers
    :param request: request instance
    :param next_func: next function
    :return:
    """
    LOGGER.info('Handling request %s %s' % (request.method, request.url.path))
    start = datetime.datetime.now()
    resp: StreamingResponse = await next_func(request)
    end = datetime.datetime.now()
    dt = end - start
    s = dt.seconds
    ms = dt.microseconds // 1000
    LOGGER.info('Handled %s %s in %s secs %s ms...' %
                (request.method, request.url.path, s, ms))
    return resp

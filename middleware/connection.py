from starlette.requests import Request
from starlette.responses import StreamingResponse
from application.logger import get_middleware_logger
import datetime

LOGGER = get_middleware_logger('CONNECTION')


async def calc_time(request: Request, nxt):
    LOGGER.info('Handling request %s %s' % (request.method, request.url.path))
    start = datetime.datetime.now()
    resp: StreamingResponse = await nxt(request)
    end = datetime.datetime.now()
    dt = end - start
    s = dt.seconds
    ms = dt.microseconds // 1000
    LOGGER.info('Handled %s %s in %s secs %s ms...' %
                (request.method, request.url.path, s, ms))
    return resp

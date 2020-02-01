from starlette.requests import Request
from starlette.responses import StreamingResponse
from application.middleware import get_logger
import datetime

LOGGER = get_logger('CONNECTION')


async def calc_time(request: Request, nxt):
    start = datetime.datetime.now()
    resp: StreamingResponse = await nxt(request)
    end = datetime.datetime.now()
    ms = (end - start).microseconds // 1000
    LOGGER.info('Handled %s %s in %s ms...' %
                (request.method, request.url.path, ms))
    return resp

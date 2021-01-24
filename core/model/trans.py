"""
Transaction models
"""
from enum import IntEnum
from typing import Callable, Any, Dict, Optional

from pydantic import BaseModel

from core.lib import time, secret, logger
from core.model.base import ExecRet

LOGGER = logger.for_model('trans')


class TransStatus(IntEnum):
    """
    transaction status
    """
    ERROR = -1
    PENDING = 0
    PROCESSING = 1
    SUCCESS = 2


TransHandler = Callable[[Any], ExecRet]


class TransExecRet(BaseModel):
    """
    exec ret of trans handler
    """
    # trans code pointed to the handler
    code: IntEnum
    # exec ret value
    value: ExecRet = ExecRet()


class TransContext(BaseModel):
    """
    transaction context
    """
    # unique session
    session: str = ''
    # trans code
    code: Optional[IntEnum] = 0
    # start time
    start_time: int = 0
    # end time
    end_time: int = 0
    # transaction status
    status: TransStatus = TransStatus.PENDING
    # handler exec ret
    ret: Optional[TransExecRet] = None

    @classmethod
    def new(cls, code: IntEnum):
        """
        create a transaction context instance by handler code
        :param code: handler code
        :return: trans ctx instance
        """
        return TransContext(
            session=secret.hs(str(time.to_microseconds())),
            start_time=time.to_milliseconds(),
            status=TransStatus.PENDING,
            ret=TransExecRet(code=code)
        )


class TransManager(BaseModel):
    """
    transaction manager
    """
    # handler map { code: handler }
    handlers: Dict[IntEnum, TransHandler] = {}

    def register_handler(self, code: IntEnum, handler: TransHandler) -> None:
        """
        register transaction handler
        :param code: handler code
        :param handler: transaction handler callback
        :return: None
        """
        self.handlers[code] = handler

    def call(self, code: IntEnum, *args, **kwargs) -> TransContext:
        """
        create a transaction
        :param code: trans code
        :param args: args for trans handler
        :param kwargs: kwargs for trans handler
        :return: the context of the handler
        """
        # create context
        ctx = TransContext.new(code)
        # check handler
        handler = self.handlers.get(code)
        if not handler:
            ctx.status = TransStatus.ERROR
            ctx.ret.value = ExecRet.err(message='failed to get handler of code %s' % code)
        else:
            # exec handler
            try:
                ctx.status = TransStatus.PROCESSING
                ret = handler(*args, **kwargs)
                if ret.success:
                    ctx.status = TransStatus.SUCCESS
                else:
                    ctx.status = TransStatus.ERROR
                ctx.ret.value = ret
            except Exception as e:
                LOGGER.exception('failed to exec handler of code %s, %s' % (code, e))
                ctx.status = TransStatus.ERROR
                ctx.ret.value = ExecRet.err(message='handler of code %s got an exception: %s' % (code, e))
        # end context
        ctx.end_time = time.to_milliseconds()
        LOGGER.info('executed transaction: %s' % ctx.json())
        return ctx

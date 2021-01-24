from enum import IntEnum
from typing import Dict, Any

from core.model.base import ExecRet


class ErrCode(IntEnum):
    """
    error codes
    """
    SUCCESS = 0
    ERROR = -1


class Resp(ExecRet):
    """
    response body
    """
    code: IntEnum = ErrCode.SUCCESS

    @classmethod
    def ok(cls, data: Any = None, message: str = '') -> Dict[str, Any]:
        """
        generate success response body
        :param data: data
        :param message: message
        :return: json dict resp body
        """
        return cls(
            success=True,
            data=data,
            message=message,
            code=ErrCode.SUCCESS
        ).dict()

    @classmethod
    def err(cls, data: Any = None, message: str = '', code: IntEnum = ErrCode.ERROR) -> Dict[str, Any]:
        """
        generate error response body with external status code 200
        :param data: data
        :param message: message
        :param code: user defined (not http) status code
        :return: json dict resp body
        """
        if code == ErrCode.SUCCESS:
            code = ErrCode.ERROR
        return cls(
            success=False,
            data=data,
            message=message,
            code=code
        ).dict()

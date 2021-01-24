"""
Basic models
"""
from typing import Tuple, Any

from pydantic import BaseModel

# basic function call return value, with only success flag and err message
PCallRet = Tuple[bool, str]


class ExecRet(BaseModel):
    """
    basic ret value for executing a specific task
    """
    success: bool = True
    message: str = ''
    data: Any = None

    @classmethod
    def ok(cls, **kwargs):
        return cls(success=True, **kwargs)

    @classmethod
    def err(cls, **kwargs):
        return cls(success=False, **kwargs)

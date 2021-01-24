"""
Time Utilities

fast approaches to commonly used time/date related functions
"""
import datetime
from typing import Optional


def now() -> datetime.datetime:
    """
    get datetime instance of time of now
    :return: time of now
    """
    return datetime.datetime.now()


def __get_t(t: Optional[datetime.datetime] = None) -> datetime.datetime:
    """
    get datetime instance
    :param t: optional datetime instance
    :return: datetime instance
    """
    return t if isinstance(t, datetime.datetime) else now()


def to_str(t: Optional[datetime.datetime] = None,
           fmt: str = '%Y-%m-%d %H:%M:%S.%f') -> str:
    """
    get string formatted time
    :param t: optional datetime instance
    :param fmt: string format
    :return:
    """
    return __get_t(t).strftime(fmt)


def to_seconds(t: Optional[datetime.datetime] = None) -> int:
    """
    datetime to seconds
    :param t: optional datetime instance
    :return: timestamp in seconds
    """
    return int(__get_t(t).timestamp())


def to_milliseconds(t: Optional[datetime.datetime] = None) -> int:
    """
    datetime to milliseconds
    :param t: datetime instance
    :return: timestamp in seconds
    """
    return int(__get_t(t).timestamp() * 10**3)


def to_microseconds(t: Optional[datetime.datetime] = None) -> int:
    """
    datetime to microseconds
    :param t: datetime instance
    :return: timestamp in seconds
    """
    return int(__get_t(t).timestamp() * 10**6)


def get_dt(start_t: datetime.datetime,
           end_t: Optional[datetime.datetime] = None) -> datetime.timedelta:
    """
    get delta time
    :param start_t: start time
    :param end_t: end time
    :return: timedelta instance
    """
    return __get_t(end_t) - start_t


def to_seconds_dt(dt: datetime.timedelta) -> int:
    """
    delta time to seconds
    :param dt: timedelta instance
    :return: seconds elapsed
    """
    return int(dt.total_seconds())


def to_milliseconds_dt(dt: datetime.timedelta) -> int:
    """
    delta time to milliseconds
    :param dt: timedelta instance
    :return: milliseconds elapsed
    """
    return int(dt.total_seconds() * 10**3)


def to_microseconds_dt(dt: datetime.timedelta) -> int:
    """
    delta time to microseconds
    :param dt: timedelta instance
    :return: microseconds elapsed
    """
    return int(dt.total_seconds() * 10**6)

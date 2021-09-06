import time

from core.lib import time as timelib
from core.lib import secret

if __name__ == '__main__':
    t = timelib.now()
    print(timelib.to_str(t))
    print(timelib.to_seconds(t))
    print(timelib.to_milliseconds(t))
    print(timelib.to_microseconds(t))
    time.sleep(3)
    dt = timelib.get_dt(t)
    print(timelib.to_seconds_dt(dt))
    print(timelib.to_milliseconds_dt(dt))
    print(timelib.to_microseconds_dt(dt))
    print(secret.randstr(8))

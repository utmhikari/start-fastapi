import json

from core.lib import secret


if __name__ == '__main__':
    s = 'username@domain.com:passWORD'
    e = secret.base64_encode(s)
    d = secret.base64_decode(e)
    print(json.dumps({
        's': s,
        'e': e,
        'd': d
    }, indent=2))

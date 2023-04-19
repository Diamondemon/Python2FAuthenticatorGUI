import base64
import hmac
import struct
import time


def hotp(key: str, counter: int, digits: int, digest: str):
    key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    counter = struct.pack('>Q', counter)
    hs = hmac.new(key, counter, digest).digest()
    offset = hs[-1] & 0x0f
    binary = struct.unpack('>L', hs[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].zfill(digits)  # taking the [digits] last numbers


def totp(key: str, time_step=30, digits=6, digest='sha1'):
    return hotp(key, int(time.time() / time_step), digits, digest)

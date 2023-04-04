import base64


def encode(data: bytes):
    return base64.b16encode(data).lower().decode()


def decode(s: str):
    return base64.b16decode(s.encode().upper())

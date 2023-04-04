

class SCryptParams:

    def __init__(self, n: int, r: int, p: int, salt: bytes):
        self.n = n
        self.r = r
        self.p = p
        self.salt = salt

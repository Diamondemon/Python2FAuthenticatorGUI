from utils import CryptoParams


class CryptoResult:

    def __init__(self, data: bytes, params: CryptoParams):
        self.data = data
        self.params = params

from utils import Hex


class CryptoParams:

    def __init__(self, nonce: bytes, tag: bytes):
        self.nonce = nonce
        self.tag = tag

    @staticmethod
    def from_json(json_obj):
        if not json_obj:
            return None
        return CryptoParams(Hex.decode(str(json_obj["nonce"])), Hex.decode(str(json_obj["tag"])))

    def to_json(self):
        return {"nonce": Hex.encode(self.nonce), "tag": Hex.encode(self.tag)}

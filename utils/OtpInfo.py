
class OtpInfo:
    ID = "otp"

    def __init__(self, secret: str, algorithm: str = "SHA1", digits: int = 6):

        self.secret = secret
        self.algorithm = algorithm
        self.digits = digits

    def get_otp(self) -> str:
        raise NotImplementedError("Base OtpInfo.get_otp method should not be called")

    @staticmethod
    def from_json(otp_type: str, json_obj: dict):
        secret = json_obj.get("secret")
        algo = json_obj.get("algo")
        digits = json_obj.get("digits")
        from utils.TotpInfo import TotpInfo
        if otp_type == TotpInfo.ID:
            return TotpInfo(secret, algo, digits, json_obj.get("period"))
        else:
            raise ValueError("Unrecognized otp type, not Totp!")

    def to_json(self):
        # TODO
        raise NotImplementedError

    def get_type(self):
        return self.ID.upper()

import base64


class OtpInfo:

    def __init__(self, secret: str, algorithm: str = "SHA1", digits: int = 6):

        self.secret = secret
        self.algorithm = algorithm
        self.digits = digits

    def get_otp(self):
        raise NotImplementedError("Base OtpInfo.get_otp method should not be called")

    @staticmethod
    def from_json(otp_type: str, json_obj: dict):
        secret = base64.b32decode(json_obj.get("secret"))
        algo = json_obj.get("algo")
        digits = json_obj.get("digits")
        from TotpInfo import TotpInfo
        if otp_type == TotpInfo.ID:
            return TotpInfo(secret, algo, digits, json_obj.get("period"))
        else:
            raise ValueError("Unrecognized otp type, not Totp!")


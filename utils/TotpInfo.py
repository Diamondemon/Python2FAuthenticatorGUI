from utils.OtpInfo import OtpInfo
from utils.otp import totp


class TotpInfo(OtpInfo):
    ID = "totp"

    def __init__(self, secret: str, algorithm: str = "SHA1", digits: int = 6, period: int = 30):
        OtpInfo.__init__(self, secret, algorithm, digits)
        self.period = period

    def get_otp(self):
        return totp(self.secret, self.period, self.digits, self.algorithm.lower())

    def to_json(self):
        return {
            "secret": self.secret,
            "algo": self.algorithm,
            "digits": self.digits,
            "period": self.period
        }

    def to_url(self):
        return f"period={self.period}&{super().to_url()}"

    def get_type(self):
        return self.ID.upper()

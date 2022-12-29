
class OtpInfo:

    def __init__(self, secret: str, algorithm: str = "SHA1", digits: int = 6):

        self.secret = secret
        self.algorithm = algorithm
        self.digits = digits

    def get_otp(self):
        print("I'm called")

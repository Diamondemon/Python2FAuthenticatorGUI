from uuid import uuid4, UUID

from utils.OtpInfo import OtpInfo
from urllib.parse import urlparse, unquote, parse_qs

from utils.TotpInfo import TotpInfo


class VaultEntry:

    def __init__(self, uuid: UUID = uuid4(), name: str = "", issuer: str = "",
                 info: OtpInfo | TotpInfo = OtpInfo(""), group: str = "",
                 usage_count: int = -1, note: str = ""):
        self._name = name
        self._issuer = issuer
        self._group = group
        self._info = info
        self._usage_count = usage_count
        self._note = note
        # self._icon
        # IconType _iconType = IconType.INVALID;
        # boolean _isFavorite;

    @staticmethod
    def from_url(url: str):
        parsing = urlparse(url)
        if parsing.scheme != "otpauth":
            raise ValueError("Not the right type of url scheme.")

        if parsing.netloc != "totp":
            raise ValueError("Not a TOTP authentication.")

        issuer, name = unquote(parsing.path).split(":")
        query = parse_qs(parsing.query)
        if query["digits"]:
            query["digits"] = int(query["digits"][0])
        else:
            query["digits"] = 6

        if query["algorithm"]:
            query["algorithm"] = query["algorithm"][0]
        else:
            query["algorithm"] = "SHA1"

        if query["secret"]:
            query["secret"] = query["secret"][0]
        else:
            raise ValueError("No secret provided!")

        if query["period"]:
            query["period"] = int(query["period"][0])
        else:
            raise ValueError("No period provided!")

        info = TotpInfo(query["secret"], query["algorithm"], query["digits"], query["period"])

        return VaultEntry(name=name, issuer=issuer, info=info)

    def get_otp(self):
        return self._info.get_otp()

    @staticmethod
    def from_json(json_obj: dict):
        if not json_obj.get("uuid"):
            entry_uuid = uuid4()
        else:
            entry_uuid = UUID(json_obj.get("uuid"))

        otp_info = OtpInfo.from_json(json_obj.get("type"), json_obj.get("info"))
        return VaultEntry(
            entry_uuid,
            json_obj.get("name"),
            json_obj.get("issuer"),
            otp_info,
            json_obj.get("group"),
            note=json_obj.get("note")
        )
        # TODO complete

    @property
    def name(self):
        return self._name

    @property
    def issuer(self):
        return self._issuer

    @property
    def period(self):
        if type(self._info) == TotpInfo:
            return self._info.period
        else:
            return 0



if __name__ == "__main__":
    entry = VaultEntry.from_url(
        "otpauth://totp/test.com%3Atest.com_du%40pont.fr?period=30&digits=6&algorithm=SHA1&secret"
        "=3PQ4AYKC3EG3DFEGRE2JGSWEVS3XO57Q&issuer=test.com")

    print(entry.get_otp())

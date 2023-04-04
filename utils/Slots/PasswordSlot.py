from uuid import UUID

from utils import CryptoUtils, Hex
from utils.CryptoParams import CryptoParams
from utils.SCryptParams import SCryptParams
from utils.Slots.Slot import Slot


class PasswordSlot(Slot):

    def __init__(self, slot_uuid: UUID, key: bytes, key_params: CryptoParams,
                 scrypt_params: SCryptParams, repaired: bool, is_backup: bool):
        super().__init__(slot_uuid, key, key_params)
        self.repaired = repaired
        self.scrypt_params = scrypt_params
        self.is_backup = is_backup

    def derive_key(self, password: str, params: SCryptParams | None = None):
        if params is None:
            return CryptoUtils.derive_key(password, self.scrypt_params)
        else:
            key = CryptoUtils.derive_key(password, params)
            self.scrypt_params = params
            return key

    def set_key(self, master_key: bytes, cipher):
        super().set_key(master_key, cipher)
        self.repaired = True

    def to_json(self):
        json_obj = super().to_json()
        json_obj["n"] = self.scrypt_params.n
        json_obj["r"] = self.scrypt_params.r
        json_obj["p"] = self.scrypt_params.p
        json_obj["salt"] = Hex.encode(self.scrypt_params.salt)
        json_obj["repaired"] = self.repaired
        json_obj["is_backup"] = self.is_backup
        return json_obj

    def get_type(self):
        return 1

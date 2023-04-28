from uuid import UUID, uuid4

from utils import CryptoUtils, Hex
from utils.CryptoParams import CryptoParams
from utils.SCryptParams import SCryptParams


class Slot:

    def __init__(self, slot_uuid: UUID, key: bytes, params: CryptoParams):
        self.uuid = slot_uuid
        self.encrypted_master_key = key
        self.encrypted_master_key_params = params

    def set_key(self, master_key: bytes, cipher):
        res = CryptoUtils.encrypt(bytes(), master_key, cipher)
        self.encrypted_master_key = res.data
        self.encrypted_master_key_params = res.params

    def get_key(self, cipher):
        res = CryptoUtils.decrypt(bytes(), self.encrypted_master_key, self.encrypted_master_key_params, cipher)
        return res.data

    @staticmethod
    def create_encrypt_cipher(key: bytes):
        return CryptoUtils.create_encrypt_cipher(key)

    def create_decrypt_cipher(self, key: bytes):
        return CryptoUtils.create_decrypt_cipher(key, self.encrypted_master_key_params.nonce)

    @staticmethod
    def from_json(json_obj: dict):
        if not json_obj.get("uuid"):
            slot_uuid = uuid4()
        else:
            slot_uuid = UUID(json_obj.get("uuid"))
        key = Hex.decode(json_obj["key"])
        key_params = CryptoParams.from_json(json_obj["key_params"])

        if json_obj["type"] == 1:
            import utils.Slots.PasswordSlot as PasswordSlot
            scrypt_params = SCryptParams(json_obj["n"], json_obj["r"], json_obj["p"], Hex.decode(json_obj["salt"]))
            repaired = json_obj.get("repaired", False)
            is_backup = json_obj.get("is_backup", False)
            return PasswordSlot.PasswordSlot(slot_uuid, key, key_params, scrypt_params, repaired, is_backup)

        raise ValueError("Wrong Slot type")

    def to_json(self):
        json_obj = {"type": self.get_type(), "uuid": str(self.uuid), "key": Hex.encode(self.encrypted_master_key),
                    "key_params": self.encrypted_master_key_params.to_json()}
        return json_obj

    def get_type(self):
        return None

    def derive_key(self, password):
        raise NotImplementedError

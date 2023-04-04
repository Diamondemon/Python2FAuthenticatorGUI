from Crypto.Random import get_random_bytes

from utils import CryptoUtils
from utils.CryptoParams import CryptoParams
from utils.Slots.SlotList import SlotList
from copy import deepcopy


class VaultFileCredentials:

    def __init__(self, master_key=get_random_bytes(32), slots: SlotList = SlotList()):
        self.master_key = master_key
        self.slots = slots

    def decrypt(self, encrypted: bytes, params: CryptoParams):
        return CryptoUtils.decrypt(self.master_key, encrypted, params)

    def encrypt(self, decrypted: bytes):
        return CryptoUtils.encrypt(self.master_key, decrypted)

    def clone(self):
        return VaultFileCredentials(self.master_key, deepcopy(self.slots))

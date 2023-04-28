from utils.Slots.PasswordSlot import PasswordSlot
from utils.Slots.Slot import Slot
from utils.Vault import Vault
from utils.VaultFile import VaultFile
from utils.VaultFileCredentials import VaultFileCredentials
from utils.VaultRepository import VaultRepository


class VaultManager:

    def __init__(self):
        self._vault_file: VaultFile | None = None
        self._repo: VaultRepository | None = None

    def init_new(self, creds: VaultFileCredentials):
        self._vault_file = None
        self._repo = VaultRepository(Vault(), creds)
        self.save()

        return self._repo

    def export(self, filename):
        if self.is_vault_loaded():
            self.repo.export(filename)

    def load_from(self, vault_file: VaultFile, creds: VaultFileCredentials | None):
        self._vault_file = None
        self._repo = VaultRepository.from_vault_file(vault_file, creds)

        return self._repo

    def load(self, creds: VaultFileCredentials):
        self.load_vault_file()

        if self.is_vault_loaded():
            return self._repo

        return self.load_from(self._vault_file, creds)

    def unlock(self, creds: VaultFileCredentials):
        return self.load_from(self._vault_file, creds)

    def lock(self, user_initiated: bool = False):
        self._repo = None
        self.load_vault_file()

    def save(self):
        self._repo.save()

    def load_vault_file(self):
        self._vault_file = VaultRepository.read_vault_file()

        if (self._vault_file is not None) and not self._vault_file.is_encrypted():
            self.load_from(self._vault_file, None)

    def is_vault_loaded(self) -> bool:
        return self._repo is not None

    def is_vault_file_loaded(self) -> bool:
        return self._vault_file is not None

    @property
    def vault_file(self):
        return self._vault_file

    @property
    def repo(self):
        return self._repo

    @property
    def is_encryption_enabled(self):
        if self.is_vault_loaded():
            return self._repo.is_encryption_enabled()
        elif self.is_vault_file_loaded():
            return self._vault_file.is_encrypted()
        else:
            return False

    @property
    def is_locked(self):
        return not self.is_vault_loaded()

    def verify_password(self, password: str):
        if self.is_vault_loaded():
            slots = self._repo.get_credentials().slots
            for slot in slots:
                if type(slots[slot]) == PasswordSlot:
                    pass_slot: PasswordSlot | Slot = slots[slot]
                    try:
                        key = pass_slot.derive_key(password)
                        pass_slot.get_key(pass_slot.create_decrypt_cipher(key))

                        return True
                    except ValueError:
                        pass
        elif self.is_vault_file_loaded():
            slots = self._vault_file.header.slots
            for slot in slots:
                if type(slots[slot]) == PasswordSlot:
                    pass_slot: PasswordSlot | Slot = slots[slot]
                    try:
                        key = pass_slot.derive_key(password)
                        pass_slot.get_key(pass_slot.create_decrypt_cipher(key))
                        return True
                    except ValueError:
                        pass
        return False

    def change_credentials(self, creds: VaultFileCredentials | None):
        self._repo = VaultRepository(self._repo.get_vault(), creds)
        self.save()

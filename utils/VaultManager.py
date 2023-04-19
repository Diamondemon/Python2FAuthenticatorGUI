from utils.Vault import Vault
from utils.VaultFile import VaultFile
from utils.VaultFileCredentials import VaultFileCredentials
from utils.VaultRepository import VaultRepository


class VaultManager:

    def __init__(self):
        self._vault_file = None
        self._repo: VaultRepository | None = None

    def init_new(self, creds: VaultFileCredentials):
        self._vault_file = None
        self._repo = VaultRepository(Vault(), creds)
        self.save()

        return self._repo

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

    def is_vault_loaded(self):
        return self._repo is not None

    def is_vault_file_loaded(self):
        return self._vault_file is not None

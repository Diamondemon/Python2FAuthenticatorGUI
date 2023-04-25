from utils.Vault import Vault
from utils.VaultFile import VaultFile
from utils.VaultFileCredentials import VaultFileCredentials


class VaultRepository:
    FILENAME = "2fa.json"
    FILEPATH = "./"

    def __init__(self, vault: Vault, creds: VaultFileCredentials):
        self._vault = vault
        self._creds = creds

    def is_encryption_enabled(self):
        return self._creds is not None

    def save(self):
        json_obj = self._vault.to_json()
        file = VaultFile()
        if self.is_encryption_enabled():
            file.set_content(json_obj, self._creds)
        else:
            file.set_content(json_obj)

        file.to_file(VaultRepository.FILEPATH + VaultRepository.FILENAME)

    def get_vault(self):
        return self._vault

    def get_credentials(self):
        return self._creds.clone()

    def set_credentials(self, creds: VaultFileCredentials = None):
        if creds is None:
            self._creds = None
        else:
            self._creds = creds.clone()

    @staticmethod
    def from_vault_file(file: VaultFile, creds: VaultFileCredentials):
        if not file.is_encrypted():
            json_obj = file.get_content()
        else:
            json_obj = file.get_content(creds)

        vault = Vault.from_json(json_obj)

        return VaultRepository(vault, creds)

    @staticmethod
    def read_vault_file():
        # TODO not hardcode
        return VaultFile.from_file(VaultRepository.FILEPATH + VaultRepository.FILENAME)

    @staticmethod
    def from_file_import(filename: str) -> VaultFile:
        return VaultFile.from_file(filename)

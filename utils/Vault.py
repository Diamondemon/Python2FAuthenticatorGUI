from utils.VaultEntry import VaultEntry


class Vault:

    def __init__(self, entries: list[VaultEntry] = []):
        super(self)

        self.entries = entries

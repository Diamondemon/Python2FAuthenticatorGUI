from utils.VaultEntry import VaultEntry


class Vault:

    def __init__(self, entries: list[VaultEntry] = []):

        self.entries = entries

    def from_json(self, json_obj):
        # TODO
        print(json_obj)

    def to_json(self):
        # TODO
        pass

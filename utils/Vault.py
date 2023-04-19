from utils.VaultEntry import VaultEntry


class Vault:

    def __init__(self, entries: list[VaultEntry] = []):

        self.entries = entries

    @staticmethod
    def from_json(json_obj):
        # TODO
        print("Hey")
        print(json_obj)
        print("Bye")

    def to_json(self):
        # TODO
        pass

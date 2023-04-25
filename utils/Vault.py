from utils.VaultEntry import VaultEntry


class Vault:

    def __init__(self, entries: list[VaultEntry] = []):

        self.entries = entries

    @staticmethod
    def from_json(json_obj):
        entries: list[VaultEntry] = []
        if json_obj["version"] != 2:
            raise ValueError(f"Incompatible Vault Version {json_obj['version']}")
        for entry in json_obj["entries"]:
            try:
                entries.append(VaultEntry.from_json(entry))
            except ValueError:
                pass
        return Vault(entries)

    def to_json(self):
        entries: list[dict] = []
        for entry in self.entries:
            entries.append(entry.to_json())
        return {"version": 2, "entries": entries}

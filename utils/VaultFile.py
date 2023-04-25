import base64
import json

from utils.Header import Header
from utils.VaultFileCredentials import VaultFileCredentials


class VaultFile:

    def __init__(self, header: Header = None, content=None):
        self.header = header
        self.content = content

    def get_content(self, creds: VaultFileCredentials = None):
        if creds is None:
            return self.content

        full = base64.b64decode(self.content)
        result = creds.decrypt(full, self.header.params)
        return json.loads(result.data.decode())

    def set_content(self, json_obj, creds: VaultFileCredentials = None):
        if creds is None:
            self.content = json_obj
            self.header = Header()
        else:
            string = json.dumps(json_obj)
            vault_bytes = string.encode()

            result = creds.encrypt(vault_bytes)
            self.content = base64.b64encode(result.data).decode()
            self.header = Header(creds.slots, result.params)

    def is_encrypted(self):
        return not self.header.is_empty()

    @staticmethod
    def from_file(filename):
        with open(filename, "r") as file:
            return VaultFile.from_json(json.load(file))

    @staticmethod
    def from_json(json_obj):
        header = Header.from_json(json_obj["header"])
        return VaultFile(header, json_obj["db"])

    def to_json(self):
        return {"header": self.header.to_json(), "db": self.content}

    def to_file(self, filename):
        with open(filename, "w") as file:
            json.dump(self.to_json(), file)

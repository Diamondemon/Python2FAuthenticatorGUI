from utils.CryptoParams import CryptoParams
from utils.Slots.SlotList import SlotList


class Header:

    def __init__(self, slots: SlotList = None, params: CryptoParams = None):
        self.slots = slots
        self.params = params

    def is_empty(self):
        return self.slots is None

    def to_json(self):
        json_obj = {}
        if self.slots is None:
            json_obj["slots"] = None
        else:
            json_obj["slots"] = self.slots.to_json()

        if self.params is None:
            json_obj["params"] = None
        else:
            json_obj["params"] = self.params.to_json()
        return json_obj

    @staticmethod
    def from_json(json_obj):
        if json_obj is None:
            return Header()

        if json_obj["version"] != 1:
            raise ValueError("Version of the file is wrong! Cannot open it.")

        return Header(SlotList.from_json(json_obj.get("slots", [])), CryptoParams.from_json(json_obj["params"]))

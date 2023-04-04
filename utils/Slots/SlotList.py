from utils.Slots.Slot import Slot


class SlotList:

    def __init__(self, slots={}):
        self.slots = slots

    @staticmethod
    def from_json(json_obj: list):
        if len(json_obj) == 0:
            return None
        slots = {}
        for json_slot in json_obj:
            slot = Slot.from_json(json_slot)
            slots[slot.uuid] = slot

    def to_json(self):
        return [slot.to_json() for slot in self.slots.values()]




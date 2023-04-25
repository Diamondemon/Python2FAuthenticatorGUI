from typing import Iterator
from uuid import UUID

from utils.Slots.Slot import Slot


class SlotList:

    def __init__(self, slots=None):
        if slots is None:
            slots: dict[UUID, Slot] = {}
        self.slots = slots

    @staticmethod
    def from_json(json_obj: list):
        if len(json_obj) == 0:
            return None
        slots = {}
        for json_slot in json_obj:
            try:
                slot = Slot.from_json(json_slot)
                slots[slot.uuid] = slot
            except ValueError as e:
                print(e)
        return SlotList(slots)

    def to_json(self):
        return [slot.to_json() for slot in self.slots.values()]

    def __iter__(self) -> Iterator[UUID]:
        return self.slots.__iter__()

    def __str__(self):
        return self.slots.__str__()

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item) -> Slot:
        return self.slots[item]

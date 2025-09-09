import json, pathlib
from dataclasses import dataclass

SAVE_PATH = pathlib.Path(__file__).resolve().parent.parent / "saves"
SAVE_PATH.mkdir(exist_ok=True) # makes a saves folder if it does not already exist

@dataclass
class GameState:
    name: str = ""
    count: int = 0
    current_slot: int | None = None

    @staticmethod
    def _slot_filename(slot: int) -> pathlib.Path:
        return SAVE_PATH / f"slot{slot}.json"

    @classmethod
    def load_slot(cls, slot: int):
        p = cls._slot_filename(slot)

        if p.exists():
            data = json.loads(p.read_text())
            return cls(name=data.get("name", ""), count=int(data.get("count", 0)), current_slot=slot)
        return cls(current_slot=slot)

    def save(self):
        if not self.current_slot:
            # Default to slot 1 if no slot has been chosen yet
            self.current_slot = 1
        p = self._slot_filename(self.current_slot)
        p.write_text(json.dumps({"name": self.name, "count": self.count}))


# Active, in-memory game state used across screens
ACTIVE_STATE = GameState()

def get_state() -> GameState:
    return ACTIVE_STATE

def load_active_slot(slot: int) -> GameState:
    global ACTIVE_STATE
    ACTIVE_STATE = GameState.load_slot(slot)
    return ACTIVE_STATE

def list_slots():
    entries = []
    for slot in (1, 2, 3):
        p = GameState._slot_filename(slot)
        if p.exists():
            data = json.loads(p.read_text())
            entries.append({"slot": slot, "name": data.get("name", ""), "count": int(data.get("count", 0))})
        else:
            entries.append({"slot": slot, "name": "", "count": 0})
    return entries
import json
import pathlib
from dataclasses import dataclass, field

SAVE_PATH = pathlib.Path(__file__).resolve().parent.parent / "saves"
SAVE_PATH.mkdir(exist_ok=True) # makes a saves folder if it does not already exist

@dataclass
class GameState:
    newGame: int = 1
    name: str = ""
    gold: int = 0
    max_health: int = 20
    health: int = max_health
    max_stamina: int = 101
    stamina: int = max_stamina
    mining_xp: int = 0
    total_xp: int = 0
    prevScreen: str = ""
    currentScreen: str = ""
    current_slot: int | None = None
    inventory: dict[str, int] = field(default_factory=lambda: {
        "stone": 0,
        "bread": 0
    })
    equipment: dict[str, dict] = field(default_factory=lambda: {
        "pickaxe": {"id": "pickaxe", "level": 1, "max_durability": 200, "curr_durability": 200}
    })

    @staticmethod
    def _slot_filename(slot: int) -> pathlib.Path:
        return SAVE_PATH / f"slot{slot}.json"

    @classmethod
    def load_slot(cls, slot: int):
        p = cls._slot_filename(slot)

        if p.exists():
            data = json.loads(p.read_text())
            return cls(newGame=int(data.get("newGame", 1)),
                       name=data.get("name", ""), 
                       gold=int(data.get("gold", 0)), 
                       max_health=int(data.get("max_health", 20)),
                       health=int(data.get("health", 20)),
                       max_stamina=int(data.get("max_health", 101)),
                       stamina=int(data.get("stamina", 101)),
                       mining_xp=int(data.get("mining_xp", 0)),
                       total_xp=int(data.get("total_xp", 0)),
                       prevScreen=data.get("prevScreen", ""),
                       currentScreen=data.get("currentScreen", ""),
                       current_slot=slot,
                       inventory=data.get("inventory", {
                           "stone": 0,
                           "bread": 0
                       }),
                       equipment=data.get("equipment", {
                           "pickaxe": {"id": "pickaxe", "level": 1, "max_durability": 200, "curr_durability": 200}
                       }))

        try:
            data = json.loads(p.read_text())
        except json.JSONDecodeError:
            return cls(current_slot=slot)

    def save(self):
        # Prevent accidental overwrite when no valid slot is selected or user is on load screen
        if self.current_slot is None or self.currentScreen == "load_game":
            return  # Skip save entirely
        
        p = self._slot_filename(self.current_slot)
        p.write_text(json.dumps({"newGame": self.newGame,
                                 "name": self.name, 
                                 "gold": self.gold,
                                 "max_health": self.max_health,
                                 "health": self.health,
                                 "max_stamina": self.max_stamina,
                                 "stamina": self.stamina,
                                 "mining_xp": self.mining_xp, 
                                 "total_xp": self.total_xp,
                                 "prevScreen": self.prevScreen,
                                 "currentScreen": self.currentScreen,
                                 "inventory": self.inventory,
                                 "equipment": self.equipment}))

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
            entries.append({"slot": slot, 
                            "name": data.get("name", ""), 
                            "currentScreen": data.get("currentScreen", "")})
        else:
            entries.append({"slot": slot, 
                            "name": "", 
                            "currentScreen": ""})
    return entries
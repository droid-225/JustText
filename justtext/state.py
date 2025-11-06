import json
import pathlib
from dataclasses import dataclass, field
from typing import Tuple
from .components.event_system import EventType

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
    attack: int = 5  # Base attack power
    defense: int = 3  # Base defense power
    current_enemy: str = ""  # ID of the enemy being fought
    play_time_seconds: float = 0.0
    mining_xp: int = 0
    combat_xp: int = 0
    total_xp: int = 0
    wilds_dist: int = 0
    wilds_event: Tuple[str, int] = ("NONE", 0)
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
                       max_stamina=int(data.get("max_stamina", 101)),
                       stamina=int(data.get("stamina", 101)),
                       attack=int(data.get("attack", 5)),
                       defense=int(data.get("defense", 3)),
                       current_enemy=data.get("current_enemy", ""),
                       play_time_seconds=float(data.get("play_time_seconds", 0.0)),
                       mining_xp=int(data.get("mining_xp", 0)),
                       combat_xp=int(data.get("combat_xp", 0)),
                       total_xp=int(data.get("total_xp", 0)),
                       wilds_dist=int(data.get("wilds_dist", 0)),
                       wilds_event=tuple(data.get("wilds_event", ("NONE", 0))),
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
                                 "play_time_seconds": self.play_time_seconds,
                                 "attack": self.attack,
                                 "defense": self.defense,
                                 "current_enemy": self.current_enemy,
                                 "mining_xp": self.mining_xp,
                                 "combat_xp": self.combat_xp,
                                 "total_xp": self.total_xp,
                                 "wilds_dist": self.wilds_dist,
                                 "wilds_event": self.wilds_event,
                                 "prevScreen": self.prevScreen,
                                 "currentScreen": self.currentScreen,
                                 "inventory": self.inventory,
                                 "equipment": self.equipment}))

    # Convenience helpers for working with wilds events in a JSON-friendly way
    def set_wilds_event(self, event_type: EventType, event_id: int) -> None:
        """Store the event as (EventType.name, id) for persistence."""
        self.wilds_event = (event_type.name, int(event_id))

    def get_wilds_event(self) -> tuple[EventType, int]:
        """Return (EventType, id). Falls back to (EventType.NONE, 0) on unknown data."""
        name, eid = self.wilds_event
        try:
            return (EventType[name], int(eid))
        except Exception:
            return (EventType.NONE, 0)

    def formatted_play_time(self) -> str:
        """Return play time as H:MM:SS formatted string."""
        total_seconds = int(self.play_time_seconds)
        hrs = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        if hrs > 0:
            return f"{hrs}:{mins:02d}:{secs:02d}"
        return f"{mins}:{secs:02d}"

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
                            "currentScreen": data.get("currentScreen", ""),
                            "play_time_seconds": data.get("play_time_seconds", 0.0)})
        else:
            entries.append({"slot": slot,
                            "name": "",
                            "currentScreen": "",
                            "play_time_seconds": 0.0})
    return entries
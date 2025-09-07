import json, pathlib
from dataclasses import dataclass

SAVES_PATH = pathlib.Path(__file__).resolve().parent.parent / "saves"
SAVES_PATH.mkdir(exist_ok=True) # makes a saves folder if it does not already exist

@dataclass
class GameState:
    count: int = 0

    @classmethod
    def load(cls, name="memory.json"):
        p = SAVES_PATH / name # path to save

        if p.exists():
            return cls(**json.load(p.read_text())) # ** turns the json file into a dictionary, cls returns the dictionary as a GameState object
        return cls() # cls is a class method, kind of like self but for a class

    def save(self, name="memory.json"):
        p = SAVES_PATH / name
        p.write_text(json.dumps({"count": self.count}))  
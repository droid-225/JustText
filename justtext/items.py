from dataclasses import dataclass
from typing import Literal, Optional, Callable
from .state import GameState

@dataclass
class ConsumableEffect:
    # Defines what happens when an itemm is used
    stamina: int = 0
    
class Consumable:
    def __init__(self, effect: ConsumableEffect):
        self.effect = effect

    def use(self, state: GameState) -> str:
        # Apply consumable effects and return result message
        if self.effect.stamina:
            state.stamina = state.stamina + self.effect.stamina

@dataclass(frozen=True)
class ItemDef:
    id: str
    name: str
    stackable: bool
    value: int = 0
    type: Literal["material", "tool", "consumable", "armor"] = "material"
    rarity: Literal["common", "mystic", "rare", "ultra rare", "legendary", "mythical", "godly"] = "common"
    # TODO: add build quality qualifers for tools and armor
    consumable_effect: ConsumableEffect | None = None

ITEMS: dict[str, ItemDef] = {
    "stone": ItemDef(id="stone", 
                     name="Stone", 
                     stackable=True, 
                     value=1, 
                     type="material", 
                     rarity="common"),
    "bread": ItemDef(id="bread", 
                     name="Bread", 
                     stackable=True, 
                     value=1, 
                     type="consumable", 
                     rarity="common", 
                     consumable_effect=ConsumableEffect(stamina=10)),
    "pickaxe": ItemDef(id="pickaxe", 
                       name="Pickaxe", 
                       stackable=False, 
                       value=0, 
                       type="tool", 
                       rarity="common")
}
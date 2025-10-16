from dataclasses import dataclass
from typing import Literal, Optional

@dataclass(frozen=True)
class ItemDef:
    id: str
    name: str
    stackable: bool
    value: int = 0
    type: Literal["material", "tool", "consumable", "armor"] = "material"
    rarity: Literal["common", "mystic", "rare", "ultra rare", "legendary", "mythical", "godly"] = "common"
    # TODO: add build quality qualifers for tools and armor

ITEMS: dict[str, ItemDef] = {
    "stone": ItemDef(id="stone", name="Stone", stackable=True, value=1, type="material", rarity="common"),
    "bread": ItemDef(id="bread", name="Bread", stackable=True, value=1, type="consumable", rarity="common"),
    "pickaxe": ItemDef(id="pickaxe", name="Pickaxe", stackable=False, value=0, type="tool", rarity="common")
}
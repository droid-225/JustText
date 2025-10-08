from ..state import get_state
from ..items import ITEMS

def item_def(item_id: str):
    return ITEMS[item_id]

# Common Getters
def get_id(item_id: str) -> str:
    return ITEMS.get(item_id).name

def is_stackable(item_id: str) -> bool:
    return ITEMS.get(item_id).stackable

def get_base_value(item_id: str) -> str:
    return ITEMS.get(item_id).value

def get_type(item_id: str) -> str:
    return ITEMS.get(item_id).type

def get_rarity(item_id: str) -> str:
    return ITEMS.get(item_id).rarity

# Inventory
def inv_add(item_id: str, qty: int = 1) -> None:
    item = ITEMS[item_id]
    state = get_state()

    if item.stackable:
        state.inventory[item_id] = state.inventory.get(item_id, 0) + qty

def inv_remove(item_id: str, qty: id) -> bool:
    state = get_state()

    if state.inventory.get(item_id, 0) < qty:
        return False
    
    state.inventory[item_id] -= qty
    
    return True

def inv_count(item_id: str) -> int:
    return get_state().inventory.get(item_id, 0)

# Equipment
def equip_equipped(slot: str) -> dict | None:
    return get_state().equipment.get(slot)

def equip_get_level(slot: str, default: int = 1) -> int:
    item = equip_equipped(slot)
    return int(item.get("level", default)) if item else default

def equip_set_level(slot: str, level: int) -> None:
    state = get_state()
    item = state.equipment.get(slot)
    if not item:
        return
    
    #max_level = ITEMS.get(item["id"]).max_level if item["id"] in ITEMS else None
    #if max_level is not None:
    #    level = min(level, max_level)
    
    item["level"] = max(level, 1)

def equip_levelup(slot: str, delta: int = 1) -> None:
    current = equip_get_level(slot)
    new_level = current + delta
    equip_set_level(slot, new_level)
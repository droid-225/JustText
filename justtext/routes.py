from typing import Callable, Dict, Any

from .screens.inn import Inn
from .screens.mine import Mine
from .screens.shop import Shop
from .screens.windhelm import Windhelm
from .screens.main_menu import Main_Menu
from .screens.new_game import New_Game
from .screens.load_game import Load_Game
from .screens.main_settings import Main_Settings
from .screens.welcome import Welcome
from .screens.inventory import Inventory
from .screens.stats import Stats
from .screens.blacksmith import Blacksmith
from .screens.wilds import Wilds
from .screens.wilds_warning import WildsWarning
from .screens.combat import Combat
from .screens.attribute import Attribute
from .state import get_state

RouteAction = Callable[[], None]

def create_routes(set_screen: Callable[[Any], None], stop: Callable[[], None]) -> Dict[str, RouteAction]:
    def go(screen_cls):
        return lambda: set_screen(screen_cls(on_select))
    
    def on_select(choice: str):
        get_state().prevScreen = get_state().currentScreen if get_state().currentScreen else ""

        # Deduct stamina only for gameplay actions. Don't drain stamina when
        # opening UI/non-action screens (inventory, stats, attribute, load/menu, etc.).
        exempt_destinations = {
            "inventory",
            "stats",
            "attribute",
            "load_game",
            "main_menu",
            "main_settings",
            "welcome_screen",
            "wilds_warning"
        }

        if choice not in exempt_destinations:
            # Only deduct stamina for actions that represent gameplay steps
            get_state().stamina -= 1

        action = routes.get(choice)
        
        if action:
            action()

    routes = {
        "main_menu": go(Main_Menu),
        "new_game": go(New_Game),
        "load_game": go(Load_Game),
        "main_settings": go(Main_Settings),
        "welcome_screen": go(Welcome),
        "mine": go(Mine),
        "windhelm": go(Windhelm),
        "shop": go(Shop),
        "inventory": go(Inventory),
        "stats": go(Stats),
        "blacksmith": go(Blacksmith),
        "attribute": go(Attribute),
        "inn": go(Inn),
        "wilds": go(Wilds),
        "wilds_warning": go(WildsWarning),
        "combat": go(Combat),
        "quit": stop
    }

    routes["__on_select__"] = on_select
    return routes
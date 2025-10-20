from typing import Callable, Dict, Any

from justtext.screens.inn import Inn
from justtext.screens.mine import Mine
from justtext.screens.shop import Shop
from justtext.screens.windhelm import Windhelm
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
from .state import get_state

RouteAction = Callable[[], None]

def create_routes(set_screen: Callable[[Any], None], stop: Callable[[], None]) -> Dict[str, RouteAction]:
    def go(screen_cls):
        return lambda: set_screen(screen_cls(on_select))
    
    def on_select(choice: str):
        get_state().prevScreen = get_state().currentScreen if get_state().currentScreen else "" 

        if (str != "inventory" and get_state().currentScreen != "inventory"
            and str != "stats" and get_state().currentScreen != "stats"):
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
        "inn": go(Inn),
        "wilds": go(Wilds),
        "wilds_warning": go(WildsWarning),
        "quit": stop
    }

    routes["__on_select__"] = on_select
    return routes
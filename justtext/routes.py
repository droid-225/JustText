from typing import Callable, Dict, Any

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

RouteAction = Callable[[], None]

def create_routes(set_screen: Callable[[Any], None], stop: Callable[[], None]) -> Dict[str, RouteAction]:
    def go(screen_cls):
        return lambda: set_screen(screen_cls(on_select))
    
    def on_select(choice: str):
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
        "quit": stop
    }

    routes["__on_select__"] = on_select
    return routes
from typing import Callable, Dict, Any
from .screens.main_menu import Main_Menu
from .screens.new_game import New_Game
from .screens.load_game import Load_Game
from .screens.main_settings import Main_Settings

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
        "quit": stop
    }

    routes["__on_select__"] = on_select
    return routes
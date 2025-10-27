from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from .options import Options

class WildsRandomEvents:
    def __init__(self, surface, yOffset=0):
        self.font = load_font()
        self.surface = surface
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.yOffset = yOffset
        
    def smallEvent(self, eventID: int):
        if eventID == 1:
            self.text.draw(self.surface, "Nothing Happened...", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 2:
            self.text.draw(self.surface, "A Wild Slime Appeared!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling", "(2) Attack the Slime"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 3:
            self.text.draw(self.surface, "You Found a Stone!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling", "(2) Collect"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 4:
            self.text.draw(self.surface, "Small Event 4 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 5:
            self.text.draw(self.surface, "Small Event 5 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)
        
    def mediumEvent(self, eventID: int):
        if eventID == 1:
            self.text.draw(self.surface, "Medium Event 1 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 2:
            self.text.draw(self.surface, "Medium Event 2 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 3:
            self.text.draw(self.surface, "Medium Event 3 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 4:
            self.text.draw(self.surface, "Medium Event 4 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 5:
            self.text.draw(self.surface, "Medium Event 5 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)

    def bigEvent(self, eventID: int):
        if eventID == 1:
            self.text.draw(self.surface, "Big Event 1 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 2:
            self.text.draw(self.surface, "Big Event 2 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 3:
            self.text.draw(self.surface, "Big Event 3 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 4:
            self.text.draw(self.surface, "Big Event 4 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)
        elif eventID == 5:
            self.text.draw(self.surface, "Big Event 5 Occured!", y_offset=self.yOffset)

            options = ["(1) Keep Traveling"]

            Options(self.surface).draw(options, yOffset=213)

    def caravan(self):
        self.text.draw(self.surface, "You have reached a friendly caravan", y_offset=self.yOffset)

        options = ["(1) Keep Traveling", 
                    "(ESC) Go to Windhelm"]

        Options(self.surface).draw(options, yOffset=213)

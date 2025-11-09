import pygame
from .base import Screen
from ..constants import GREEN, WHITE
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state

class Attribute(Screen):
    def __init__(self, on_select, on_complete=None):
        self.font = load_font()
        self.on_select = on_select
        self.on_complete = on_complete  # callback when stats are confirmed
        self.text = TextRenderer(self.font)
        self.selected_stat = 0  # 0=str, 1=dex, 2=wil, 3=int
        self.state = get_state()
        self.state.currentScreen = "attribute"
        self.stat_names = ["Strength", "Dexterity", "Willpower", "Intelligence"]
        self.stat_descriptions = [
            "Increases physical damage and carrying capacity",
            "Improves dodge chance and critical hits",
            "Enhances stamina recovery and magic resistance",
            "Increases magic damage and skill effectiveness"
        ]

    def get_stat_value(self, index):
        if index == 0: return self.state.strength
        elif index == 1: return self.state.dexterity
        elif index == 2: return self.state.willpower
        else: return self.state.intelligence

    def set_stat_value(self, index, value):
        if index == 0: self.state.strength = value
        elif index == 1: self.state.dexterity = value
        elif index == 2: self.state.willpower = value
        else: self.state.intelligence = value

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE and self.on_complete:
            # Only allow escape if we're allocating points after character creation
            self.on_complete()
            return

        if event.key == pygame.K_UP:
            self.selected_stat = (self.selected_stat - 1) % 4
        elif event.key == pygame.K_DOWN:
            self.selected_stat = (self.selected_stat + 1) % 4
        elif event.key == pygame.K_RIGHT and self.state.stat_points > 0:
            # Increase selected stat
            current = self.get_stat_value(self.selected_stat)
            self.set_stat_value(self.selected_stat, current + 1)
            self.state.stat_points -= 1
        elif event.key == pygame.K_LEFT:
            # Decrease selected stat (but not below 1)
            current = self.get_stat_value(self.selected_stat)
            if current > 1:
                self.set_stat_value(self.selected_stat, current - 1)
                self.state.stat_points += 1
        elif event.key == pygame.K_RETURN and self.state.stat_points == 0:
            # Only allow confirmation when all points are spent
            if self.on_complete:
                self.on_complete()
            else:
                self.on_select("windhelm")  # Default to starting town
        elif event.key == pygame.K_SPACE:
            self.on_select("stats")

    def draw(self, surface):
        # Reset layout each frame so text doesn't accumulate off-screen
        self.text.reset_layout(left_margin=20)

        # Title and available points
        # Use first_line=True so the title does not advance the layout before drawing
        self.text.draw(surface, "Character Stats", color=GREEN, alignment="middle", first_line=True)
        self.text.draw(surface, f"Available Points: {self.state.stat_points}")

        # Small spacer
        self.text.addOffset("y", 6)

        # Draw each stat with its value and description
        for i, (name, desc) in enumerate(zip(self.stat_names, self.stat_descriptions)):
            color = GREEN if i == self.selected_stat else WHITE
            value = self.get_stat_value(i)

            # Stat name and value
            stat_text = f"{name}: {value}"
            # Draw the stat name (new line)
            self.text.draw(surface, stat_text, color=color)
            # Draw the description on the next line, indented
            self.text.draw(surface, desc, l_offset=20)

        # Draw controls with a small gap before them
        self.text.addOffset("y", 8)
        self.text.draw(surface, "↑/↓: Select Stat")
        self.text.draw(surface, "←/→: Adjust Points")
        if self.state.stat_points == 0:
            self.text.draw(surface, "ENTER: Confirm")
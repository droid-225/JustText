import pygame
from .base import Screen
from ..constants import WHITE, GREEN
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..util.leveling import LevelCalculator

class Stats(Screen): # Stats screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.state.currentScreen = "stats"
        self.prevScreen = self.state.prevScreen

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state.stamina += 1
                self.on_select(self.prevScreen)
            elif event.key == pygame.K_SPACE:
                # Always allow opening the attribute/stat allocation screen
                self.on_select("attribute")

    def draw(self, surface):
        self.state.total_xp = self.state.mining_xp + self.state.combat_xp
        totalLevelCalc = LevelCalculator()
        minigLevelCalc = LevelCalculator(base_xp=10)
        combatLevelCalc = LevelCalculator(base_xp=15)

        level = totalLevelCalc.calculate_level(self.state.total_xp)
        mining_level = minigLevelCalc.calculate_level(self.state.mining_xp)
        combat_level = combatLevelCalc.calculate_level(self.state.combat_xp)
        prevScreen = self.prevScreen

        xp_for_next_level = totalLevelCalc.get_xp_for_next_level(self.state.total_xp)
        mining_xp_for_next_level = minigLevelCalc.get_xp_for_next_level(self.state.mining_xp)
        combat_xp_for_next_level = combatLevelCalc.get_xp_for_next_level(self.state.combat_xp)
        
        self.text.reset_layout()
        self.text.draw(surface, "<~~~~~~~~~~ Statistics ~~~~~~~~~~>", GREEN, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)

        self.text.draw(surface, f"Health: {self.state.health}/{self.state.max_health}", WHITE)
        self.text.draw(surface, f"Play Time: {self.state.formatted_play_time()}", WHITE)

        self.text.draw(surface, f"Level: {level}", WHITE)
        self.text.draw(surface, f"XP Needed to Level Up: {xp_for_next_level}", GREEN, l_offset=30)
        
        self.text.draw(surface, f"Mining Level: {mining_level}", WHITE)
        self.text.draw(surface, f"XP Needed to Level Up: {mining_xp_for_next_level}", GREEN, l_offset=30)
        
        self.text.draw(surface, f"Combat Level: {combat_level}", WHITE)
        self.text.draw(surface, f"XP Needed to Level Up: {combat_xp_for_next_level}", GREEN, l_offset=30)
        self.text.addOffset("y", 10)

        # Display character stats
        self.text.draw(surface, "Character Stats:", WHITE)
        self.text.draw(surface, f"Strength: {self.state.strength}", WHITE, l_offset=20)
        self.text.draw(surface, f"Dexterity: {self.state.dexterity}", WHITE, l_offset=20)
        self.text.draw(surface, f"Willpower: {self.state.willpower}", WHITE, l_offset=20)
        self.text.draw(surface, f"Intelligence: {self.state.intelligence}", WHITE, l_offset=20)
        
        # Show stat points if available
        if self.state.stat_points > 0:
            self.text.draw(surface, f"Stat Points Available: {self.state.stat_points}", GREEN)
            self.text.draw(surface, "(SPACE) Allocate Stat Points", GREEN)
        
        self.text.addOffset("y", 10)
        self.text.draw(surface, f"(ESC) Return to {prevScreen.capitalize()}", WHITE, alignment="bottom")
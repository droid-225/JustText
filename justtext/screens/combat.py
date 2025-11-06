import pygame
from .base import Screen
from ..constants import RED, WHITE, GREEN, BLUE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..components.footer import Footer
from ..components.options import Options
from ..components.entity_system import EntitySystem, EntityType
from ..util.itemUtil import inv_add
import random

class Combat(Screen):
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.state.currentScreen = "combat"
        
        # Initialize entity system and get enemy data
        self.entity_system = EntitySystem()
        self.enemy = self.entity_system.get_entity(self.state.current_enemy)
        self.enemy_current_health = self.enemy.stats.health
        
        # Combat state
        self.turn_message = ""
        self.can_act = True  # Controls if player can take action
    
    def handle_combat_turn(self, action: str):
        """Handle a single turn of combat"""
        if not self.can_act:
            return
            
        self.can_act = False  # Prevent multiple actions until turn is complete
        
        # Player's turn
        damage_dealt = max(0, self.state.attack - self.enemy.stats.defense)
        if action == "attack":
            self.enemy_current_health -= damage_dealt
            self.turn_message = f"You deal {damage_dealt} damage to the {self.enemy.name}!"
        elif action == "defend":
            # Increase defense temporarily for enemy's turn
            self.state.defense += 2
            self.turn_message = "You take a defensive stance!"
            
        # Check if enemy is defeated
        if self.enemy_current_health <= 0:
            self.handle_victory()
            return
            
        # Enemy's turn
        enemy_damage = max(0, self.enemy.stats.attack - self.state.defense)
        self.state.health -= enemy_damage
        self.turn_message += f"\nThe {self.enemy.name} deals {enemy_damage} damage to you!"
        
        # Reset temporary defense bonus if defending
        if action == "defend":
            self.state.defense -= 2
            
        # Check if player is defeated
        if self.state.health <= 0:
            self.handle_defeat()
            return
            
        self.can_act = True  # Allow next action
        self.update(0)  # Refresh display
        
    def handle_victory(self):
        """Handle enemy defeat"""
        # Award XP and gold
        self.state.xp += self.enemy.stats.xp_value
        self.state.gold += self.enemy.stats.gold_value
        
        # Handle drops
        if self.enemy.drops:
            for item_id, chance in self.enemy.drops.items():
                if random.random() < chance:
                    inv_add(item_id, 1)
        
        # Save state and return to wilds
        self.state.save()
        self.on_select("wilds")
        
    def handle_defeat(self):
        """Handle player defeat"""
        # Lose half gold and return to town
        self.state.gold = self.state.gold // 2
        self.state.health = self.state.max_health // 2  # Restore some health
        self.state.save()
        self.on_select("windhelm")

    def handle_event(self, event):
        if not self.can_act:  # Ignore inputs if still processing last action
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:  # Attack
                self.handle_combat_turn("attack")
            elif event.key == pygame.K_2:  # Defend
                self.handle_combat_turn("defend")
            elif event.key == pygame.K_3:  # Run (with chance of failure)
                if random.random() < 0.7:  # 70% chance to escape
                    self.state.save()
                    self.on_select("wilds")
                else:
                    self.turn_message = "Couldn't escape!"
                    self.handle_combat_turn("none")  # Enemy still gets their turn

    def update(self, dt: float = 0):
        if hasattr(self, 'surface'):
            self.draw(self.surface)

    def draw(self, surface):
        self.surface = surface
        self.text.reset_layout()
        
        # Draw combat header
        self.text.draw(surface, "==== COMBAT ====", color=RED, bg=BLACK, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)
        
        # Draw enemy info
        self.text.draw(surface, f"{self.enemy.name}", l_offset=10)
        self.text.draw(surface, f"HP: {self.enemy_current_health}/{self.enemy.stats.health}", l_offset=10)
        self.text.draw(surface, f"ATK: {self.enemy.stats.attack} DEF: {self.enemy.stats.defense}", l_offset=10)
        self.text.addOffset("y", 6)
        
        # Draw player info
        self.text.draw(surface, "Your Stats:", l_offset=10)
        self.text.draw(surface, f"HP: {self.state.health}/{self.state.max_health}", l_offset=10)
        self.text.draw(surface, f"ATK: {self.state.attack} DEF: {self.state.defense}", l_offset=10)
        self.text.addOffset("y", 6)
        
        # Draw turn message if any
        if self.turn_message:
            self.text.draw(surface, self.turn_message, l_offset=10)
            self.text.addOffset("y", 6)
        
        # Draw combat options
        options = [
            "(1) Attack",
            "(2) Defend",
            "(3) Run"
        ]
        Options(surface).draw(options, yOffset=213)
        
        Footer(surface).draw()
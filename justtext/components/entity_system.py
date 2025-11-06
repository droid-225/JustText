from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Optional, List

class EntityType(Enum):
    """Types of entities that can exist in the game."""
    MONSTER = auto()
    FRIENDLY = auto()
    NEUTRAL = auto()

class InteractionType(Enum):
    """Types of interactions an entity can support."""
    FIGHT = auto()
    TALK = auto()
    TRADE = auto()
    PET = auto()
    FEED = auto()

@dataclass
class EntityStats:
    """Core stats that entities can have."""
    health: int
    max_health: int
    attack: int
    defense: int
    level: int
    xp_value: int  # XP gained when defeating this entity
    gold_value: int  # Gold dropped when defeating this entity

@dataclass
class EntityInteraction:
    """Defines an interaction possibility with an entity."""
    type: InteractionType
    description: str  # What happens when this interaction is chosen
    requirements: Dict[str, int] = None  # e.g. {"level": 5, "item_id": "bread"}

@dataclass
class Entity:
    """Represents any interactive entity in the game."""
    id: str  # unique identifier e.g. "slime_basic"
    name: str
    type: EntityType
    description: str
    stats: EntityStats
    interactions: List[EntityInteraction]
    drops: Dict[str, float] = None  # item_id -> drop chance (0-1)
    friendly: bool = False

class EntitySystem:
    """Central system for managing game entities and their definitions."""
    
    def __init__(self):
        self.entities: Dict[str, Entity] = {
            # Basic slime - first enemy type
            "slime_basic": Entity(
                id="slime_basic",
                name="Slime",
                type=EntityType.MONSTER,
                description="A basic green slime. Seems harmless enough.",
                stats=EntityStats(
                    health=10,
                    max_health=10,
                    attack=2,
                    defense=1,
                    level=1,
                    xp_value=5,
                    gold_value=2
                ),
                interactions=[
                    EntityInteraction(
                        type=InteractionType.FIGHT,
                        description="The slime bounces menacingly!"
                    ),
                    EntityInteraction(
                        type=InteractionType.PET,
                        description="It's squishy but oddly pleasant to pet."
                    ),
                    EntityInteraction(
                        type=InteractionType.FEED,
                        description="The slime happily absorbs the food.",
                        requirements={"item_id": "bread"}
                    )
                ],
                drops={
                    "slime_goo": 0.7,  # 70% chance to drop goo
                    "rare_core": 0.05  # 5% chance to drop rare core
                }
            ),
            
            # Friendly merchant - example of non-hostile NPC
            "merchant_wandering": Entity(
                id="merchant_wandering",
                name="Wandering Merchant",
                type=EntityType.FRIENDLY,
                description="A friendly merchant who wanders the wilds.",
                stats=EntityStats(
                    health=20,
                    max_health=20,
                    attack=0,
                    defense=2,
                    level=5,
                    xp_value=0,
                    gold_value=0
                ),
                interactions=[
                    EntityInteraction(
                        type=InteractionType.TALK,
                        description="The merchant greets you warmly."
                    ),
                    EntityInteraction(
                        type=InteractionType.TRADE,
                        description="The merchant shows you their wares."
                    )
                ],
                friendly=True
            )
        }
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get an entity definition by ID."""
        return self.entities.get(entity_id)
    
    def get_entities_by_type(self, entity_type: EntityType) -> List[Entity]:
        """Get all entities of a specific type."""
        return [e for e in self.entities.values() if e.type == entity_type]
    
    def get_entities_by_level(self, min_level: int, max_level: int) -> List[Entity]:
        """Get entities within a level range."""
        return [e for e in self.entities.values() 
                if min_level <= e.stats.level <= max_level]
    
    def get_friendly_entities(self) -> List[Entity]:
        """Get all friendly entities."""
        return [e for e in self.entities.values() if e.friendly]
    
    def get_hostile_entities(self) -> List[Entity]:
        """Get all hostile (non-friendly) entities."""
        return [e for e in self.entities.values() if not e.friendly]
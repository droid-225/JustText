from dataclasses import dataclass
from typing import List, Callable, Optional
from enum import Enum, auto

class EventType(Enum):
    SMALL = auto()
    MEDIUM = auto()
    BIG = auto()
    CARAVAN = auto()

@dataclass
class EventOption:
    key: str  # e.g. "1", "2", "ESC"
    text: str
    action: str  # action identifier e.g. "keep_traveling", "collect", "attack"
    enabled: bool = True

@dataclass
class Event:
    id: int
    type: EventType
    description: str
    options: List[EventOption]
    
    def get_available_options(self) -> List[EventOption]:
        return [opt for opt in self.options if opt.enabled]

class EventSystem:
    def __init__(self):
        self.events = {
            # Small Events
            (EventType.SMALL, 1): Event(
                id=1,
                type=EventType.SMALL,
                description="Nothing Happened...",
                options=[
                    EventOption("1", "Keep Traveling", "keep_traveling")
                ]
            ),
            (EventType.SMALL, 2): Event(
                id=2,
                type=EventType.SMALL,
                description="A Wild Slime Appeared!",
                options=[
                    EventOption("1", "Keep Traveling", "keep_traveling"),
                    EventOption("2", "Attack the Slime", "attack")
                ]
            ),
            (EventType.SMALL, 3): Event(
                id=3,
                type=EventType.SMALL,
                description="You Found a Stone!",
                options=[
                    EventOption("1", "Keep Traveling", "keep_traveling"),
                    EventOption("2", "Collect", "collect")
                ]
            ),
            # Medium Events (placeholders)
            (EventType.MEDIUM, 1): Event(
                id=1,
                type=EventType.MEDIUM,
                description="Medium Event 1 Occurred!",
                options=[EventOption("1", "Keep Traveling", "keep_traveling")]
            ),
            (EventType.MEDIUM, 2): Event(
                id=2,
                type=EventType.MEDIUM,
                description="Medium Event 2 Occurred!",
                options=[EventOption("1", "Keep Traveling", "keep_traveling")]
            ),
            (EventType.MEDIUM, 3): Event(
                id=3,
                type=EventType.MEDIUM,
                description="Medium Event 3 Occurred!",
                options=[EventOption("1", "Keep Traveling", "keep_traveling")]
            ),
            (EventType.MEDIUM, 4): Event(
                id=4,
                type=EventType.MEDIUM,
                description="Medium Event 4 Occurred!",
                options=[EventOption("1", "Keep Traveling", "keep_traveling")]
            ),
            (EventType.MEDIUM, 5): Event(
                id=5,
                type=EventType.MEDIUM,
                description="Medium Event 5 Occurred!",
                options=[EventOption("1", "Keep Traveling", "keep_traveling")]
            ),
            # Big Events (placeholders)
            (EventType.BIG, 1): Event(
                id=1,
                type=EventType.BIG,
                description="Big Event 1 Occurred!",
                options=[EventOption("1", "Keep Traveling", "keep_traveling")]
            ),
            (EventType.BIG, 2): Event(
                id=2,
                type=EventType.BIG,
                description="Big Event 2 Occurred!",
                options=[EventOption("1", "Keep Traveling", "keep_traveling")]
            ),
            (EventType.BIG, 3): Event(
                id=3,
                type=EventType.BIG,
                description="Big Event 3 Occurred!",
                options=[EventOption("1", "Keep Traveling", "keep_traveling")]
            ),
            (EventType.BIG, 4): Event(
                id=4,
                type=EventType.BIG,
                description="Big Event 4 Occurred!",
                options=[EventOption("1", "Keep Traveling", "keep_traveling")]
            ),
            (EventType.BIG, 5): Event(
                id=5,
                type=EventType.BIG,
                description="Big Event 5 Occurred!",
                options=[EventOption("1", "Keep Traveling", "keep_traveling")]
            ),
        }
        
        # Special case for caravan
        self.caravan_event = Event(
            id=0,
            type=EventType.CARAVAN,
            description="You have reached a friendly caravan",
            options=[
                EventOption("1", "Keep Traveling", "keep_traveling"),
                EventOption("ESC", "Go to Windhelm", "goto_windhelm")
            ]
        )
    
    def get_event(self, event_type: EventType, event_id: int) -> Optional[Event]:
        return self.events.get((event_type, event_id))
    
    def get_caravan_event(self) -> Event:
        return self.caravan_event
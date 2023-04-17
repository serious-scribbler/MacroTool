
from dataclasses import dataclass
from enum import Enum

class XKeyEventType(Enum):
    """Defines the type of a key event
    """

    RELEASE = 0
    """represents a key release
    """

    PRESS = 1
    """represents a key press
    """

@dataclass
class XKeyEvent:

    keycode: int
    """The keycode for this event
    """
    event_type: XKeyEventType
    """The event type of the event
    """

    duration: int = 0
    """The duration of the event in ms
    """

    key_name: str = "unknown"
    """The name of the key
    """
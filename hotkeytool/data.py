from screeninfo import get_monitors
from dataclasses import dataclass
from enum import Enum


def get_primary_coordinates() -> tuple[int, int]:
    """Returns coordinates on the top left corner of the primary screen

    Returns:
        tuple[int, int]: The x and y position for notifications and windows
    """
    for screen in get_monitors():
        if screen.is_primary:
            x = screen.x + 20
            y = screen.y + int(screen.height*0.1)
            return(x, y)
    return (20, 40)

class ActionType(Enum):
    """Describes the type of a hokey"""

    COMMAND = 1
    """Hotkeys with this type represent commands"""

    MACRO = 2
    """Hotkeys with this type represent macros which are text strings that are automatically typed out"""

    PROGRAMM = 3
    """Hotkeys with this type launch a programm"""

@dataclass
class HotKey():
    """Dataclass to represent hotkeys, the key itself is not included since HotKeys are stored in a map"""

    hk_type: ActionType
    """The type of the current hotkey, view the docs for ActionType for more information"""

    value: str
    """The value of the given hotkey, either a command, macro string or program name with arguments"""

    name: str
    """This name is shown on screen, when the macro is executed"""

@dataclass
class Settings():
    """Dataclass to hold the programm settings
    """

    terminal_command: str
    """The command to open a terminal on the current system"""

    overlay_duration: int
    """The duration in ms for which self-closing overlays are displayed"""

    window_x: int
    """The top left x coordinate of the on-screen position of the windows drawn by this program"""

    window_y: int
    """The top left y coordinate of the on-screen position of the windows drawn by this program"""
from dataclass import dataclass
from enum import Enum

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
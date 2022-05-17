from .handler import *
from .ui.overlay import TextOverlay, OverlayWindow, create_notification_window
from .data import Settings, get_primary_coordinates
from time import sleep


# TODO: Implement the actual tool
pos = get_primary_coordinates()
print(pos)
s = Settings("xfce4-terminal -e 'bash -c \"", 3000, pos[0], pos[1])
create_notification_window(s, True, "Hotkeytool started!")
mm = MacroManager(s)
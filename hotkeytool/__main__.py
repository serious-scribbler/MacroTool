from .handler import *
from .ui.overlay import TextOverlay, OverlayWindow
from .data import Settings, get_primary_coordinates

pos = get_primary_coordinates()
print(pos)
s = Settings("xfc4-terminal", 5000, pos[0], pos[1])
o = OverlayWindow(s, False)
o.run()
t = TextOverlay(s, True, "Hello World!")
t.run()
#MacroManager("xfce4-terminal")
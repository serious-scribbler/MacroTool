from .handler import *
from .ui.overlay import TextOverlay, OverlayWindow
from .data import Settings

s = Settings("xfc4-terminal", 5000)
o = OverlayWindow(s, False)
o.run()
t = TextOverlay(s, True, "Hello World!")
t.run()
#MacroManager("xfce4-terminal")
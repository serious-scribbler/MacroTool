from .handler import *
from .ui.overlay import TextOverlay, OverlayWindow, create_notification_window
from .data import Settings, get_primary_coordinates
from time import sleep


# TODO: Implement the actual tool
pos = get_primary_coordinates()
print(pos)
s = Settings("xfc4-terminal", 5000, pos[0], pos[1])
create_notification_window(s, True, "Multiprocessed notification!")
w = create_notification_window(s, False, "Multiprocessed notification 2!", 1)
i = 0
while True:
    print(".")
    sleep(1)
    i += 1
    if i == 10:
        w.terminate()
        w.join()
        exit(0)
#MacroManager("xfce4-terminal")
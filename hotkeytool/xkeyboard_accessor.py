from Xlib.display import Display
import Xlib
from Xlib import X
from Xlib import XK
import sys
import signal
from Xlib.protocol.event import KeyPress, KeyRelease
import time
from .key_helpers import XKeyEventType, XKeyEvent

class XKeyboardAccessor():

    def __init__(self):
        pass

    def press_key(self, keycode, display = None, window = None) -> None:
        if not display:
            display = Display()
        if not window:
            display.get_input_focus()._data["focus"]
        event = KeyPress(
            time = int(time.time()),
            root = display.screen().root,
            window = window,
            same_screen = 0,
            child = X.NONE,
            root_x = 0,
            root_y = 0,
            event_x = 0,
            event_y = 0,
            state = 0,
            detail = keycode
        )
        window.send_event(event, propagate = True)
    
    def release_key(self, keycode, display = None, window = None) -> None:
        if not display:
            display = Display()
        if not window:
            window = display.get_input_focus()._data["focus"]
        event = KeyRelease(
            time = int(time.time()),
            root = display.screen().root,
            window = window,
            same_screen = 0,
            child = X.NONE,
            root_x = 0,
            root_y = 0,
            event_x = 0,
            event_y = 0,
            state = 0,
            detail = keycode
        )
        window.send_event(event, propagate = True)

    def execute_events(self, events: list[XKeyEvent]) -> None:
        """Executes the given list of XKeyEvents

        Args:
            events (list[XKeyEvent]): A list of XKeyEvents that shall be executed
        """
        display = Display()
        window = display.get_input_focus()._data["focus"]
        for event in events:
            if event.event_type = XKeyEventType.PRESS:
                self.press_key(keycode, display, window)
            else:
                self.release_key(keycode, display, window)
            os.sleep(event.duration / 1000)
        display.sync()
        display.close()

if __name__ == "__main__":
    helper = XKeyboardAccesor()
    print("sleeping")
    time.sleep(3)
    print("typing...")
    helper.sendString("ich habe augen")
    helper.sendString("und du")
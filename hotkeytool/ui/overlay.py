import tkinter as tk
from hotkeytool.data import Settings
from multiprocessing import Process

def create_notification_window(settings: Settings, autoclose:bool, text: str, y_offset: int = 0) -> Process:
    """Launches a notification window in it's own process

    Args:
        settings (Settings): The application settings
        autoclose (bool): Wether or not to autoclose the window
        text (str): The notification text
        y_offset (int, optional): _description_. Defaults to 0.
    Returns:
        Process: _description_
    """
    p = Process(target=__create_notification, args=(settings, autoclose, text, y_offset))
    p.start()
    return p


def __create_notification(settings: Settings, autoclose: bool, text: str, y_offset: int):
    # Creates a notification overlay
    window = TextOverlay(settings, autoclose, text, y_offset)
    window.run()

class OverlayWindow():
    """The Base class for all overlay windows
    """
    def __init__(self, settings:Settings, autoclose:bool, y_offset: int= 0):
        self.settings = settings
        self.autoclose = autoclose
        self.root = tk.Tk()
        self.root.configure(bg="grey12")
        self.root.attributes('-type', 'splash') # Workaround for overrideredirect not working
        #self.root.overrideredirect(True) # Disables window decorations, doesn#t work on manjaro-xfce (window invisible)
        self.root.geometry("+" + str(self.settings.window_x) + "+" + str(self.settings.window_y + y_offset * 100)) # Places the overlay at the top left of the screen TODO: Center horizontally
        self.root.lift() # Display the window above all other windows
        self.root.wm_attributes("-topmost", True) # Stay on top
        self.root.wm_attributes("-alpha", 0.8) # Opacity, requires compositor included in xfce4
        self.border = tk.Frame(self.root, borderwidth=3, background="red")
        self.content_padding = tk.Frame(self.border, borderwidth=0, background="grey12")
        self.content = tk.Frame(self.content_padding, borderwidth=0, background="grey12")

        if not self.autoclose:
            self.close_label = tk.Label(
                self.content,
                text=" X",
                font=("Liberation Mono Bold", 18),
                fg="red2",
                bg="grey12"
            )
            self.close_label.bind("<Button-1>", self.close)
            self.close_label.grid(row=0, column=1)
        
        
    def run(self):
        if self.autoclose:
            self.root.after(self.settings.overlay_duration, self.close)
        self.content_padding.pack()
        self.content.pack(padx=10, pady=10)
        self.border.pack()
        self.root.mainloop()


    def close(self, *args):
        self.root.destroy()
    

class TextOverlay(OverlayWindow):

    def __init__(self, settings: Settings, autoclose: bool, text: str, y_offset: int = 0):
        super().__init__(settings, autoclose, y_offset)
        self.text = text
        self.label = tk.Label(
            self.content,
            text=self.text,
            font=("Liberation Mono Bold", 18),
            fg="snow1",
            bg="grey12"
        )
        self.label.grid(row=0, column=0)
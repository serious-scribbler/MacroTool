import tkinter as tk
from hotkeytool.data import Settings

class OverlayWindow():
    """The Base class for all overlay windows
    """
    def __init__(self, settings:Settings, autoclose:bool):
        self.settings = settings
        self.autoclose = autoclose
        self.root = tk.Tk()
        self.root.configure(bg="grey12")
        self.root.attributes('-type', 'splash') # Workaround for overrideredirect not working
        #self.root.overrideredirect(True) # Disables window decorations, doesn#t work on manjaro-xfce (window invisible)
        self.root.geometry("+15+15") # Places the overlay at the top left of the screen TODO: Center horizontally
        self.root.lift() # Display the window above all other windows
        self.root.wm_attributes("-topmost", True) # Stay on top
        self.root.wm_attributes("-alpha", 0.8) # Opacity, requires compositor included in xfce4

        if not self.autoclose:
            self.close_label = tk.Label(
                self.root,
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

        self.root.mainloop()

    def close(self, *args):
        self.root.destroy()
    

class TextOverlay(OverlayWindow):

    def __init__(self, settings, autoclose, text):
        super().__init__(settings, autoclose)
        self.text = text
        self.label = tk.Label(
            self.root,
            text=self.text,
            font=("Liberation Mono Bold", 18),
            fg="snow1",
            bg="grey12"
        )
        self.label.grid(row=0, column=0)
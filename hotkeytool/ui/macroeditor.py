import tkinter as tk
import tkinter.tkk as tkk

from hotkeytool.data import Macro, Settings, ActionType

class MacroEditor():

    def __init__(self, edit_macro: Macro):
        self.root = tk.Tk()
        self.root.configure(bg="grey12")
        self.root.lift() # Display the window above all other windows
        self.root.wm_attributes("-topmost", True) # Stay on top
        self.root.geometry("600x400")
        self.root.title("HotkeyTool - " + edit_macro.key_combination)

        self.macro = edit_macro

        
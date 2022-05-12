import tkinter as tk
import tkinter.ttk as ttk

from hotkeytool.data import HotKey, Settings, ActionType

editor_font = "Liberation Mono Bold"
class MacroEditor():

    def __init__(self, edit_macro: HotKey):
        self.root = tk.Tk()
        self.root.lift() # Display the window above all other windows
        self.root.wm_attributes("-topmost", True) # Stay on top
        self.root.geometry("800x500")
        self.root.title("HotkeyTool - " + edit_macro.key_combination)
        self.root.eval("tk::PlaceWindow . center")
        self.macro = edit_macro

        self.macroLabel = self.close_label = tk.Label(
            self.root,
            text="Edit " + self.macro.key_combination,
            font=(editor_font, 18),
        )
        self.macroLabel.grid(row=0, column=0, columnspan= 5, sticky="NESW", ipadx=4, ipady=4) # Try N = North?
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)
        
        for i in range(5):        
            self.root.grid_columnconfigure(i, weight=1)

        self.type_label = self.close_label = tk.Label(
            self.root,
            text="Action type:",
            font=(editor_font, 12),
        )
        self.cmd_label = self.close_label = tk.Label(
            self.root,
            text="Command/Program/Macro:",
            font=(editor_font, 12),
        )

        self.name_label = tk.Label(
            self.root,
            text="Macro Name",
            font=(editor_font, 12),
        )
        self.name_label.grid(row=1, column=0, columnspan=2, padx=4, pady=4)

        self.macro_name = tk.StringVar(value=self.macro.name)
        self.name_entry = tk.Entry(self.root, textvariable=self.macro_name, font=("Liberation Mono", 12), exportselection=0)
        self.name_entry.grid(row=1, column=2, columnspan=3, padx=4, pady=4, sticky="nesw")

        self.type_label.grid(row=2, column=0, columnspan=2, padx=4, pady=4, sticky="sew")
        self.cmd_label.grid(row=2, column=2, columnspan=3, padx=4, pady=4, sticky="sew")

        self.macro_types = ["COMMAND", "MACRO", "PROGRAM"]
        self.current_type_selection = tk.StringVar(value=self.macro.hk_type.name)
        self.macro_type_menu = tk.OptionMenu(self.root, self.current_type_selection, *self.macro_types)
        self.macro_type_menu.grid(row=3, column=0, padx=4, pady=4, columnspan=2, sticky="new")

        self.current_command = tk.StringVar(value=self.macro.value)
        self.command_textbox = tk.Entry(self.root, textvariable=self.current_command, font=("Liberation Mono", 12), exportselection=0)
        self.command_textbox.grid(row=3, column=2, columnspan=3, rowspan=2, padx=4, pady=4, sticky="nesw")

        self.cancel_btn = tk.Button(self.root, text="Cancel", font=(editor_font, 12), command=self.cancel)
        self.apply_btn = tk.Button(self.root, text ="Apply", font=(editor_font, 12), command=self.apply)

        self.cancel_btn.grid(row=5, column=1, padx=4, pady=4)
        self.apply_btn.grid(row=5, column=3, padx=4, pady=4)
        
        self.root.mainloop()
    
    def cancel(self):
        self.root.destroy()

    def apply(self):
        self.macro.name = self.macro_name.get()

        match self.current_type_selection.get():
            case "COMMAND":
                self.macro.hk_type = ActionType.COMMAND
            case "MACRO":
                self.macro.hk_type = ActionType.MACRO
            case _:
                self.macro.hk_type = ActionType.PROGRAMM
        
        self.macro.value = self.current_command.get()
        self.root.destroy()
        print(self.macro)

import keyboard
import subprocess
from subprocess import DETACHED_PROCESS, CREATE_NEW_PROCESS_GROUP, CREATE_BREAKAWAY_FROM_JOB, DEVNULL
import shlex

from .data import ActionType, HotKey
class MacroManager():

    def __init__(self, terminal_command):
        # TODO: Read Macros from json
        self.macros = {}
        self.terminal_cmd = terminal_command

    def record_hotkey(self):
        # TODO: Display recording dialog
        hk = keyboard.read_hotkey()
        if hk in self.macros:
            print("Macro already exists!") # TODO: Display on screen
        else:
            pass # TODO: Display macro action selection
    

    def edit_hotkey(self):
        # TODO Display "Press you hotkey to edit it"
        hk = keyboard.read_hotkey()
        if hk not in self.macros:
            print("Macro doesn't exist")
        else:
            pass # TODO: open macro selection with old settings selected

    
    def execute_macro(self, hk: str):
        macro = self.macros[hk]

        if macro.hk_type is ActionType.COMMAND:
            # TODO: Display message (or maybe not?)
            self.launch_terminal(macro.value)
        elif macro.hk_type is ActionType.PROGRAMM:
            # TODO: Display message
            self.launch_programm(macro.value)
        else:
            # TODO: Display message (or maybe not?)
            keyboard.write(macro.value)
    

    def launch_programm(self, name_and_args: str):
        args = shlex.split(name_and_args, posix=False)
        subprocess.Popen(args, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_BREAKAWAY_FROM_JOB)


    def launch_terminal(self, command: str):
        # TODO: Check if shell=True needs to be used
        args = [self.terminal_cmd]
        args.append(command)
        subprocess.Popen(args, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_BREAKAWAY_FROM_JOB)
import keyboard
import subprocess
import shlex
from time import sleep

from .data import ActionType, HotKey
class MacroManager():

    def __init__(self, terminal_command):
        # TODO: Read Macros from json
        self.macros = {}
        self.terminal_cmd = terminal_command
        self.keys_down = set()
        self.keys_were_down = set()
        self.recordmode = False
        self.editmode = False
        keyboard.hook(self.hook_callback)
        keyboard.wait("windows+control+shift+q")

    def record_hotkey(self):
        # TODO: Display recording dialog
        sleep(4)
        print("Enter Hotkey")
        hk = keyboard.read_hotkey()
        print(hk)
        if hk in self.macros:
            print("Macro already exists!") # TODO: Display on screen
        else:
            pass # TODO: Display macro action selection
    

    def edit_hotkey(self):
        # TODO Display "Press you hotkey to edit it"
        sleep(0.5)
        hk = keyboard.read_hotkey()
        print(hk)
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
        subprocess.Popen(args, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_BREAKAWAY_FROM_JOB)


    def launch_terminal(self, command: str):
        # TODO: Check if shell=True needs to be used
        args = [self.terminal_cmd]
        args.append(command)
        subprocess.Popen(args, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_BREAKAWAY_FROM_JOB)


    # TODO: HINT: Look at keyboard.key_to_scan_codes
    def hook_callback(self, event: keyboard.KeyboardEvent):
        if event.event_type == "down":
            if event.scan_code not in self.keys_down:
                # suppress modified keys (E.g. shift+1 gets reported as ! on a german keyboard)
                self.keys_down.add(event.scan_code)
                if len(self.keys_down) >= len(self.keys_were_down):
                    # The longest pressed combination as the wanted combination
                    self.keys_were_down = self.keys_down.copy()
        else:
            if event.scan_code in self.keys_down:
                self.keys_down.remove(event.scan_code)

        if len(self.keys_down) == 0:
            # Hotkey entered
            if len(self.keys_were_down) < 2:
                return # No key combination, reset not necessary since any key press will override keys_were_down
            keynames = []
            for k in self.keys_were_down:
                keynames.append(self.get_scancode_name(k))
            
            self.keys_were_down.clear() # Reset keys_were_down
            key_combination = self.parse_key_combination(keynames)

            self.handle_combination(key_combination)


    def handle_combination(self, key_combination: str):
        print(key_combination)
        if self.recordmode:
            self.recordmode = False
            # TODO: hide message, show config dialogue


        if self.editmode:
            self.editmode = False
            # TODO: hide message, show config dialogue

        if key_combination == "windows+ctrl+shift+r":
            # TODO: display message
            self.recordmode = True
        
        if key_combination == "windows+ctrl+shift+e":
            # TODO: display message
            self.recordmode = True



    def get_scancode_name(self, code) -> str:
        return keyboard._os_keyboard.to_name[(code, ())][0]


    def parse_key_combination(self, keynames: list[str]) -> str:
        key_combination = ""

        for name in ["windows", "ctrl", "shift", "alt"]:
            if name in keynames:
                keynames.remove(name)
                if key_combination != "":
                    key_combination += "+"
                key_combination += name
        
        for key in sorted(keynames):
            if key_combination != "":
                key_combination += "+"
            key_combination += key
        
        return key_combination
import keyboard
import subprocess
import shlex
from time import sleep
from .data import ActionType, HotKey, Settings
from .ui.overlay import create_notification_window
class MacroManager():
    """The MacroManager handles keyboard inputs and manages macros
    """

    def __init__(self, settings: Settings):
        """Creates and starts a macro monitor with the given settings

        Args:
            terminal_command (settings): Contains Settings for terminal commands and notifications
        """
        # TODO: Read Macros from json
        self.macros = {}
        self.settings = settings
        self.keys_down = set()
        self.keys_were_down = set()
        self.recordmode = False
        self.editmode = False
        self.notification_processes: list[Process] = []
        self.persistent_message: Process = None
        keyboard.hook(self.hook_callback)
        keyboard.wait("windows+control+shift+q")
        for p in self.notification_processes:
            p.terminate()
            p.join()

    def record_hotkey(self):
        sleep(4)
        print("Enter Hotkey")
        hk = keyboard.read_hotkey()
        print(hk)
        if hk in self.macros:
            print("Macro already exists!") # TODO: Display on screen
        else:
            pass # TODO: Display macro action selection
    

    def edit_hotkey(self):
        sleep(0.5)
        hk = keyboard.read_hotkey()
        print(hk)
        if hk not in self.macros:
            print("Macro doesn't exist")
        else:
            pass # TODO: open macro selection with old settings selected

    
    def _kill_notification_processes(self):
        for p in self.notification_processes:
            p.join(timeout=0)
            if not p.is_alive():
                self.notification_processes.remove(p)

    
    def execute_macro(self, hk: str):
        macro = self.macros[hk]

        self._kill_notification_processes()
        
        if macro.hk_type is ActionType.COMMAND:
            self.launch_terminal(macro.value)
        elif macro.hk_type is ActionType.PROGRAMM:
            self._create_notification("Executed '" + macro.name + "'")
            self.launch_programm(macro.value)
        else:
            keyboard.write(macro.value)
    

    def launch_programm(self, name_and_args: str):
        # TODO: Test
        args = shlex.split(name_and_args, posix=False)
        subprocess.Popen(args, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_BREAKAWAY_FROM_JOB)


    def launch_terminal(self, command: str):
        # TODO: Check if shell=True needs to be used
        # TODO: Test
        args = [self.terminal_cmd]
        args.append(command)
        subprocess.Popen(args, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_BREAKAWAY_FROM_JOB)


    def hook_callback(self, event: keyboard.KeyboardEvent):
        """Callback hook for the keyboard library, handles all keyevent and detects key combinations

        Args:
            event (keyboard.KeyboardEvent): The event that triggered the hook
        """
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


    def _create_notification(self, text: str):
        prcs = create_notification_window(self.settings, True, text, y_offset=len(self.notification_processes))
        self.notification_processes.append(prcs)


    def _create_persistent_message(self, text: str):
        prcs = create_notification_window(self.settings, False, text, y_offset=len(self.notification_processes))
        self.persistent_message = prcs


    def _hide_persistent_message(self):
        self.persistent_message.terminate()
        self.persistent_message.join()
        self.persistent_message = None


    def handle_combination(self, key_combination: str):
        """Handles the given key combination

        Args:
            key_combination (str): _description_
        """
        print(key_combination)
        if self.recordmode:
            self.recordmode = False
            self._hide_persistent_message()
            # TODO: how config dialogue
            self._create_notification("Hotkey registered:\n'" + key_combination + "'")
            return

        if self.editmode:
            self.editmode = False
            self._hide_persistent_message()
            # TODO: show config dialogue
            self._create_notification("Hotkey registered:\n'" + key_combination + "'")
            return

        if key_combination == "windows+ctrl+shift+r":
            self._create_persistent_message("Press and release a key combination\nto create a new macro")
            self.recordmode = True
        
        if key_combination == "windows+ctrl+shift+e":
            self._create_persistent_message("Press and release a key combination\nto edit the corresponding macro")
            self.editmode = True
        
        if key_combination in self.macros:
            self.execute_macro(key_combination)



    def get_scancode_name(self, code) -> str:
        """Returns the name of the key with the given scancode

        Args:
            code : The scancode of the selected key

        Returns:
            str: The name of the given key
        """
        return keyboard._os_keyboard.to_name[(code, ())][0]


    def parse_key_combination(self, keynames: list[str]) -> str:
        """Parses a list of pressed keys into a readable key combination string

        Args:
            keynames (list[str]): A list of keys that were pressed

        Returns:
            str: A human readable key combination string
        """
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
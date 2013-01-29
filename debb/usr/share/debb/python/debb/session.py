import xdg.DesktopEntry
import os
import Launcher
import sys
import time

def start(window_manager="xmonad", restarts_count = 3):
    applications_entries = __calculate_applications_entries()
    autostart_entries = __calculate_autostart_entries().values()
    for autostart_entry in autostart_entries:
        try:
            if autostart_entry.get("X-DEBB-Autostart-enabled") != "false":
                Launcher.launch(autostart_entry)
        except:
            pass
    while restarts_count > 0:
        process = Launcher.launch(applications_entries[window_manager])
        while True:
            time.sleep(0.5)
            poll = process.poll()
            if poll is not None:
                if poll == 0:
                    restarts_count = 0
                break
        restarts_count -= 1

def close():
    __session_open = False

def __calculate_entries(dirs, location):
    entries = {}
    for directory in dirs:
        try:
            entries_dir = directory + '/' + location
            for desktop_entry_file in os.listdir(entries_dir):
                if desktop_entry_file.endswith(".desktop"):
                    desktop_entry_name = desktop_entry_file[:desktop_entry_file.rfind(".desktop")]
                    if not entries.has_key(desktop_entry_name):
                        try:
                            entry = xdg.DesktopEntry.DesktopEntry();
                            entry.parse(entries_dir + "/" + desktop_entry_file)
                            entries[desktop_entry_name] = entry;
                        except:
                            pass
        except:
            pass
    return entries

def __calculate_applications_entries():
    return __calculate_entries(xdg.DesktopEntry.xdg_data_dirs, "applications")

def __calculate_autostart_entries():
    return __calculate_entries(xdg.DesktopEntry.xdg_config_dirs, "autostart")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        start(sys.argv[1])
    else:
        start()
    

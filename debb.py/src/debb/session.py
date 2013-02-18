import xdg.DesktopEntry
import os
import launcher
import sys
import time

__autostart_entries = {}
__application_entries = {}

def start(window_manager="i3", restarts_count = 3):
    __application_entries = __calculate_applications_entries()
    __autostart_entries = __calculate_autostart_entries().values()
    for autostart_entry in __autostart_entries:
        try:
            if autostart_entry.get("X-DEBB-Autostart-enabled") != "false":
                launcher.launch(autostart_entry)
        except:
            pass
    while restarts_count > 0:
        process = launcher.launch(__application_entries[window_manager])
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


import xdg.DesktopEntry
import os
from debb import Launcher
import shlex
import sys

__session_open = True

def start(window_manager="xmonad"):
    applications_entries = __calculate_applications_entries()
    #autostart_entries = __calculate_autostart_entries().values()
    #for v in autostart_entries:
    #    Launcher.launch(v)
    while __session_open:
        Launcher.launch_and_wait(applications_entries[window_manager])

def close():
    __session_open = False

def __calculate_entries(dirs, location):
    entries = {}
    for dir in dirs:
        try:
            entries_dir = dir + '/' + location
            for desktop_entry_file in os.listdir(entries_dir):
                if not entries.has_key(desktop_entry_file) and desktop_entry_file.endswith(".desktop"):
                    try:
                        desktop_entry_name = desktop_entry_file[:desktop_entry_file.rfind(".desktop")]
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
    if len(sys.argv) != 2:
        print "Syntax: session <window_manager_app>"
        sys.exit()
    start(sys.argv[1])

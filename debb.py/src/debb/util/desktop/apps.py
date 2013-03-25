import xdg
import os

def _calculate_entries(dirs, location):
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

def _calculate_applications_entries():
    return _calculate_entries(xdg.DesktopEntry.xdg_data_dirs, "applications")

def _calculate_autostart_entries():
    return _calculate_entries(xdg.DesktopEntry.xdg_config_dirs, "autostart")

entries = _calculate_applications_entries()

autostart_entries = _calculate_autostart_entries()

def get_applications():
    return entries

def add_application(application):
    raise NotImplemented()

def remove_application(application):
    raise NotImplemented()

def get_autostart_applications():
    return autostart_applications

def add_autostart_application(application):
    raise NotImplemented()

def remove_autostart_application(application):
    raise NotImplemented()

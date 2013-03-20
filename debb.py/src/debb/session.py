import xdg.DesktopEntry
import os
from util import launcher
import sys
from debb.util.dbuswrappers import wrapper
from debb.util.dbuswrappers import consolekit
from gi.repository import GObject
import dbus.service
import threading

_autostart_entries = {}
application_entries = {}

def start(window_manager="x-terminal-emulator", restarts_count=3):
    
    mainloop = GObject.MainLoop()
    process = None
    
    dbus_session = wrapper.session
    
    def calculate_entries(dirs, location):
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
    
    def calculate_applications_entries():
        return calculate_entries(xdg.DesktopEntry.xdg_data_dirs, "applications")
    
    def calculate_autostart_entries():
        return calculate_entries(xdg.DesktopEntry.xdg_config_dirs, "autostart")
    
    class Session(dbus.service.Object):

        @dbus.service.method("debb.Session")
        def start(self):
            self._restarts_count = 3
            application_entries = calculate_applications_entries()
            autostart_entries = calculate_autostart_entries().values()
            
            for autostart_entry in _autostart_entries:
                try:
                    if autostart_entry.get("X-DEBB-Autostart-enabled") != "false":
                        launcher.launch(autostart_entry)
                except:
                    pass
            while self._restarts_count > 0:
                self._process = launcher.launch(application_entries[window_manager])
                while True:
                    result = self._process.wait()
                    if result is not None:
                        if result == 0:
                            self._restarts_count = 0
                        break
                self._restarts_count -= 1
        
        @dbus.service.method("debb.Session")
        def stop(self):
            self._restarts_count = 0
            self._process.kill()
    
    if any("debb.Session" == name for name in dbus_session.list_names()):
        print "Session already running"
        dbus_session.debb_Session.Session.debb_Session.start()
        return
    
    dbus_session.request_name("debb.Session")
    Session(dbus_session, "/Session")
    threading.Thread(target=mainloop.run).start()
    

def close():
    __session_open = False

if __name__ == "__main__":
    if len(sys.argv) == 2:
        start(sys.argv[1])
    else:
        start()


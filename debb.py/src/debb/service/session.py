import dbus.service
import xdg.DesktopEntry
import os
import threading

from debb.util.dbus import wrapper as bus
from debb.util.dbus import consolekit
from debb.util.desktop import launcher 
from debb.util.desktop import apps
from debb.util.common import conf as conf_util

from gi.repository import GObject

def start(window_manager=None):

    dbus_session = bus.session
    
    mainloop = GObject.MainLoop()

    settings = conf_util.create("debb.Session")

    def open_session(self):
        for application in apps.autostart_entries:
            launcher.launch(apps.autostart_entries[application])
        self._process = launcher.launch(apps.entries[settings["window-manager"]])
        result = self._process.wait()
        GObject.idle_add(self.on_close, result)
            
                
    class Session(dbus.service.Object):

        def __init__(self, restarts_count, *args, **kwargs):
            dbus.service.Object.__init__(self, *args, **kwargs)
            self._process = None
            self._restarts_count = restarts_count
            

        @dbus.service.method("debb.Session")
        def open(self):
            if self._process is not None:
                raise ValueError("Session is already running")
            threading.Thread(target=open_session, args=(self)).start()
        
        @dbus.service.signal("debb.Session")
        def on_close(self, result):
            self._process = None
            if result != 0 and self._restarts_count > 0:
                self._restarts_count -= 1
                self.open()
                
        @dbus.service.method("debb.Session")
        def close(self):
            if self._process is None:
                raise ValueError("Session is not started")
            launcher.kill_all()
            
        @dbus.service.method("debb.Session")
        def start(self, application):
            launcher.launch(apps.entries[application])
            
            
    if dbus_session.is_service_running("debb.Session"):
        print "Service already running"
        return
            
    GObject.threads_init()
    dbus_session.request_name("debb.Session")
    Session(3, dbus_session, "/")
    mainloop.run()

if __name__ == "__main__":
    start(window_manager="gvim")

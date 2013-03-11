import sys
import dbus

from debb.util import session as session_util
from debb.util import dbusfactory as dbusfactory_util
import os
from gi.repository import GObject

def start(window_manager="i3", restarts_count=3):
    dbusfactory = dbusfactory_util.create()
    dbus_system = dbusfactory.system_bus()
    
    util = session_util.create()
    cookie = util.open()
    
    os.environ['XDG_SESSION_COOKIE'] = cookie
    
    def idle_hint_changed(hint):
        print "idle: " + hint
    
    dbus_system.add_signal_receiver(idle_hint_changed, "IdleHintChanged", "org.freedesktop.ConsoleKit.Session", "org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit")
    
    util.get_current_session()
    
    mainloop = GObject.MainLoop()
    mainloop.run()
    
    util.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        start(sys.argv[1])
    else:
        start()


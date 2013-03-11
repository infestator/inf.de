import dbus
from debb.util import dbusfactory

def create():
    
    factory = dbusfactory.create()
    dbus_session = factory.session_bus()
    dbus_system = factory.system_bus()
    
    consolekit_object = dbus_system.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
    consolekit = dbus.Interface(consolekit_object, "org.freedesktop.ConsoleKit.Manager")

    class util:
        
        def open(self):
            return consolekit.OpenSession()
        
        def close(self):
            consolekit.CloseSession()
            
        def get_current_session(self):
            print consolekit.GetCurrentSession()
    
    return util()

if __name__ == "__main__":
    util = create()

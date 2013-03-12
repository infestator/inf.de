import dbus.mainloop.glib

def create():
    glibMainloop = dbus.mainloop.glib.DBusGMainLoop()

    class DBusFactory:

        def system_bus(self):
            return dbus.SystemBus(mainloop=glibMainloop)

        def session_bus(self):
            return dbus.SessionBus(mainloop=glibMainloop)
        
    return DBusFactory()

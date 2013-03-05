import dbus.mainloop.glib

def create():
    glibMainloop = dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    class DBusFactory:

        def system_bus(self):
            return dbus.SystemBus(mainloop=glibMainloop)

        def session_bus(self):
            return dbus.SessionBus(glibMainloop)
        
    return DBusFactory()
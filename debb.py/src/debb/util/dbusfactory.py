import dbus.mainloop.glib

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

def create_system_bus():
    return dbus.SystemBus()

def create_session_bus():
    return dbus.SessionBus()
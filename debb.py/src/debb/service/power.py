import dbus
import threading
import gobject
import dbus.service
import dbus.mainloop.glib
import debb.util.power
import gtk

started = False


#upower_object = dbus_system.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
#upower = dbus.Interface(upower_object, "org.freedesktop.UPower")
#upower_properties = dbus.Interface(upower_object, "org.freedesktop.DBus.Properties")

def start():
    gtk.gdk.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    dbus_session = dbus.SessionBus()
    
    class PowerService(dbus.service.Object):

        @dbus.service.signal("debb.Power")        
        def changed(self, device):
            print device

        @dbus.service.method("debb.Power")
        def emit(self):
            self.changed("hello")
    
    def changed():
        print "changed"
    
    if any("debb.Power" == name for name in dbus_session.list_names()):
        print "Service already running"
        powerService = dbus.Interface(dbus_session.get_object("debb.Power", "/Service"), "debb.Power")
        powerService.emit()
        return

    mainLoop = gobject.MainLoop()
    
    threading.Thread(target=mainLoop.run).start()
    dbus_system = dbus.SystemBus(mainloop=mainLoop)
    
    dbus_session.request_name("debb.Power")
    PowerService(dbus_session, "/Service")
    dbus_system.add_signal_receiver(changed)
#    dbus_system.add_signal_receiver(handler, "Changed", "org.freedesktop.UPower", "org.freedesktop.UPower", "/org/freedesktop/UPower")

if __name__ == '__main__':
    start()
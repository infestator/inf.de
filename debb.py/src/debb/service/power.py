import gobject
import dbus.service
from debb.util import power as power_util

def start():
    dbus_session = dbus.SessionBus()
    
    class Power(dbus.service.Object):
        pass
        
    def changed():
        if power_util.is_lid_closed():
            if power_util.is_on_battery():
                power_util.hibernate()
            else:
                power_util.suspend()

    if any("debb.Power" == name for name in dbus_session.list_names()):
        print "Service is already running"
        return

    mainloop = gobject.MainLoop()

    dbus_system = dbus.SystemBus()

    dbus_session.request_name("debb.Power")
    Power(dbus_session, "/")
    dbus_system.add_signal_receiver(changed, "Changed", "org.freedesktop.UPower", "org.freedesktop.UPower", "/org/freedesktop/UPower")
    mainloop.run()

if __name__ == '__main__':
    start()

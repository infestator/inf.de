"""

Utility for working with power management through DBus from userspace

"""
from debb.util.dbuswrappers import upower
from debb.util.dbuswrappers import consolekit
from debb.util.dbuswrappers import wrapper

def create():
    upower_object = wrapper.system.upower.upower
    upower_upower = upower_object.upower
    upower_properties = upower_object.properties
    
    consolekit_object = wrapper.system.consolekit.consolekit
    consolekit_manager = consolekit_object.consolekit

    class Util:

        def suspend(self):
            upower_upower.Suspend()

        def hibernate(self):
            upower_upower.Hibernate()

        def shutdown(self):
            return consolekit_manager.Stop()

        def restart(self):
            return consolekit_manager.Restart()

        def is_suspend_allowed(self):
            return upower_upower.SuspendAllowed()

        def is_hibernate_allowed(self):
            return upower_upower.HibernateAllowed()

        def is_shutdown_allowed(self):
            return consolekit_manager.CanStop()

        def is_restart_allowed(self):
            return consolekit_manager.CanRestart()

        def is_on_battery(self):
            return upower_properties.Get("org.freedesktop.UPower", 'OnBattery')

        def is_lid_present(self):
            return upower_properties.Get("org.freedesktop.UPower", 'LidIsPresent')

        def is_lid_closed(self):
            return upower_properties.Get("org.freedesktop.UPower", 'LidIsClosed')
        
        def connect_on_change_listener(self, listener):
            upower_object.connect_to_signal("Changed", listener, str(upower_object.upower))

    return Util()

"""

Utility for working with power management through DBus from userspace

"""
import dbus
from debb.util import dbusfactory

def create():
    dbus_system = dbusfactory.create().system_bus()

    upower_object = dbus_system.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
    upower = dbus.Interface(upower_object, "org.freedesktop.UPower")
    upower_properties = dbus.Interface(upower_object, "org.freedesktop.DBus.Properties")

    consolekit_object = dbus_system.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
    consolekit = dbus.Interface(consolekit_object, "org.freedesktop.ConsoleKit.Manager")

    class Util:

        def suspend(self):
            return upower.Suspend()

        def hibernate(self):
            return upower.Hibernate()

        def shutdown(self):
            return consolekit.Stop()

        def restart(self):
            return consolekit.Restart()

        def is_suspend_allowed(self):
            return bool(upower.SuspendAllowed())

        def is_hibernate_allowed(self):
            return bool(upower.HibernateAllowed())

        def is_shutdown_allowed(self):
            return bool(consolekit.CanStop())

        def is_restart_allowed(self):
            return bool(consolekit.CanRestart())

        def is_on_battery(self):
            return bool(upower_properties.Get("org.freedesktop.UPower", 'OnBattery'))

        def is_lid_present(self):
            return bool(upower_properties.Get("org.freedesktop.UPower", 'LidIsPresent'))

        def is_lid_closed(self):
            return bool(upower_properties.Get("org.freedesktop.UPower", 'LidIsClosed'))

    return Util()

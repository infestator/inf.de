"""

Utility for working with power management through DBus from userspace

"""

import dbus

dbus_system = dbus.SystemBus()

upower_object = dbus_system.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
upower = dbus.Interface(upower_object, "org.freedesktop.UPower")
upower_properties = dbus.Interface(upower_object, "org.freedesktop.DBus.Properties")

consolekit_object = dbus_system.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
consolekit = dbus.Interface(consolekit_object, "org.freedesktop.ConsoleKit.Manager")

def suspend():
    return upower.Suspend()

def hibernate():
    return upower.Hibernate()

def shutdown():
    return consolekit.Stop()

def restart():
    return consolekit.Restart()

def is_suspend_allowed():
    return bool(upower.SuspendAllowed())

def is_hibernate_allowed():
    return bool(upower.HibernateAllowed())

def is_shutdown_allowed():
    return bool(consolekit.CanStop())

def is_restart_allowed():
    return bool(consolekit.CanRestart())

def is_on_battery():
    return bool(upower_properties.Get("org.freedesktop.UPower", 'OnBattery'))

def is_lid_present():
    return bool(upower_properties.Get("org.freedesktop.UPower", 'LidIsPresent'))

def is_lid_closed():
    return bool(upower_properties.Get("org.freedesktop.UPower", 'LidIsClosed'))

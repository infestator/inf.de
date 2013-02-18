import dbus
import time
import threading

dbus_system = dbus.SystemBus()

upower_object = dbus_system.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
upower = dbus.Interface(upower_object, "org.freedesktop.UPower")
upower_properties = dbus.Interface(upower_object, "org.freedesktop.DBus.Properties")

def suspend():
    return upower.Suspend()

def hibernate():
    return upower.Hibernate()

def is_suspend_allowed():
    return bool(upower.SuspendAllowed())

def is_hibernate_allowed():
    return bool(upower.HibernateAllowed())

def is_on_battery():
    return bool(upower_properties.Get("org.freedesktop.UPower", 'OnBattery'))

def is_lid_present():
    return bool(upower_properties.Get("org.freedesktop.UPower", 'LidIsPresent'))

def is_lid_closed():
    return bool(upower_properties.Get("org.freedesktop.UPower", 'LidIsClosed'))

def _run():
    while True:
        if is_lid_present():
            if is_lid_closed():
                suspend()
        time.sleep(0.5);

def start():
    threading.Thread(target=_run).start()

if __name__ == '__main__':
    start()
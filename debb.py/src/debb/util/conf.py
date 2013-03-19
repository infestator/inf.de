from debb.util import dbusfactory
from dbus.exceptions import DBusException
import dbus

from gi.repository import Gtk, Gio, GLib
import os

def create(app):
    source = Gio.SettingsSchemaSource.new_from_directory(os.environ['DEBB_HOME'] + "/share/schemas", None, True)
    schema = source.lookup(app, True)
    settings = Gio.Settings.new_full(schema, None, None)

    # Fix to work with enums    
    original__setitem__ = settings.__setitem__
    def __setitem__(self, name, value):
        try:
            original__setitem__(name, value)
        except NotImplementedError:
            settings.set_value(name, GLib.Variant('s', value))
    Gio.Settings.__setitem__ = __setitem__

    return settings

if __name__ == "__main__":
    settings = create("debb.power-service")
    settings["lid-close-action-ac"] = 'suspend'
    settings["lid-close-action-battery"] = 'suspend'
    print settings["lid-close-action-ac"]
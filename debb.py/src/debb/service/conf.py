from debb.util import dbusfactory
from dbus.exceptions import DBusException
import dbus

from gi.repository import Gtk, Gio, GLib
import os

def create(app):
    source = Gio.SettingsSchemaSource.new_from_directory(os.environ['HOME'] + "/src/inf/repositories/inf.de/debb.meta/schemas", None, True)
    schema = source.lookup(app, True)
    settings = Gio.Settings.new_full(schema, None, None)
    return settings

if __name__ == "__main__":
#    config = create("test")
#    config.set("/test/name/qwertyasdfgh", "value")
#    print config.get("name")
#    source = Gio.SettingsSchemaSource.new_from_directory(os.environ['HOME'] + "/tmp/schemas", None, True)
#    schema = source.lookup("com.companyname.appname", True)
#    settings = Gio.Settings.new_full(schema, None, None)
#    print settings.get_value("mybool").unpack()
    settings = create("debb.power-service")
    value = settings["lid-close-action"]
    print value
    settings["lid-close-action"] = 1
#    print settings["lid-close-action"]
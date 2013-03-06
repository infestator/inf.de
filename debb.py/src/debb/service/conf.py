from debb.util import dbusfactory
from dbus.exceptions import DBusException
import dbus

from gi.repository import Gtk, Gio

def create(app):
    bus = dbusfactory.create().session_bus()
    
    try:
        bus.get_name_owner("ca.desrt.dconf")
    except DBusException:
        bus.activate_name_owner("ca.desrt.dconf")
    
    writer_object = bus.get_object("ca.desrt.dconf", "/ca/desrt/dconf/Writer/user")
    writer_properties = dbus.Interface(writer_object, "ca.desrt.dconf.Writer")
        
    class Conf:
        
        def get_all(self):
            return writer_properties.GetAll("ca.desrt.dconf.WriterInfo")
        
        def get(self, name):
            return writer_properties.Get("ca.desrt.dconf.WriterInfo", name)
        
        def set(self, name, value):
            writer_properties.Write(name, [value])
            
    return Conf()
    
    
if __name__ == "__main__":
    config = create("test")
    config.set("/test/name/qwertyasdfgh", "value")
    print config.get("name")
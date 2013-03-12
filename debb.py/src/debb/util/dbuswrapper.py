import dbus
import dbus.mainloop.glib

def enum(**enums):
    return type('Enum', (), enums)

TYPE = enum(Session=1, System=2)

def create(name_dict={}, path_dict={}, interface_dict={}, type=TYPE.Session):
    glibMainloop = dbus.mainloop.glib.DBusGMainLoop()

    bus = {
            TYPE.Session: dbus.SystemBus,
            TYPE.System: dbus.SystemBus
        }[type](mainloop=glibMainloop)

    class Wrapper:

        def __init__(self):
            self._cache = {}
            self._dict = {}

        def set_dict(self, dict):
            self._dict = dict.copy()
            
        def dict_append(self, dict):
            self._dict.update(dict)

        def resolve_attr(self, attr):
            if self._cache.has_key(attr):
                return self._cache[attr]
            elif self._dict.has_key(attr):
                formatted_attr = self._dict[attr]
            else:
                formatted_attr = self.format_attr(attr)
            return formatted_attr 

        def __getattr__(self, attr):
            attr_object = self.getattr(self.resolve_attr(attr))
            self._cache[attr] = attr_object
            return attr_object

        def getattr(self, formatted_attr):
            raise NotImplementedError()

        def format_attr(self, attr):
            raise NotImplementedError()

    class DBus(Wrapper):
        
        def __init__(self):
            Wrapper.__init__(self)
            self.set_dict(name_dict)
    
        def format_attr(self, attr):
            return attr.replace('_', '.')
        
        def getattr(self, name):
            
            class DBusName(Wrapper):
                
                def __init__(self):
                    Wrapper.__init__(self)
                    self.set_dict(path_dict)

                def format_attr(self, attr):
                    return '/' + attr.replace('_', '/')
        
                def getattr(self, path):
                    
                    dbus_object = bus.get_object(name, path)

                    class DBusObject(Wrapper):

                        def __init__(self):
                            Wrapper.__init__(self)
                            self.set_dict(interface_dict)

                        def format_attr(self, attr):
                            return attr.replace('_', '.')
        
                        def subscribe(self, signal, handler, interface):
                            print dbus_object.connect_to_signal(signal, handler, self.resolve_attr(interface))
        
                        def getattr(self, interface):
                            return dbus.Interface(dbus_object, interface)

                    return DBusObject()

            return DBusName()

    return DBus()

if __name__ == "__main__":
    bus = create(
                 name_dict={"ConsoleKit": "org.freedesktop.ConsoleKit"},
                 path_dict={"Manager": "/org/freedesktop/ConsoleKit/Manager"},
                 interface_dict={"Manager": "org.freedesktop.ConsoleKit.Manager"}
             )
    interface_dict={"Manager1": "org.freedesktop.ConsoleKit.Manager"}
    iface = bus.ConsoleKit.Manager
    iface.dict_append(interface_dict)
    
    def handler(*args):
        print "Handler"
    
    manager = bus.ConsoleKit.Manager.Manager1
    iface.subscribe("IdleHintChanged", handler, "Manager")
    print manager.GetCurrentSession()

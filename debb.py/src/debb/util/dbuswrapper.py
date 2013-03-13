import dbus
import dbus.mainloop.glib

def _create(bus):
    class Wrapper:

        def __init__(self):
            self._cache = {}
            self.aliases = {}

        def resolve_attr(self, attr):
            if self._dict.has_key(attr):
                formatted_attr = self.aliases[attr]
            else:
                formatted_attr = self.decode_attr(attr)
            return formatted_attr

        def __getattr__(self, attr):
            if self._cache.has_key(attr):
                return self._cache[attr]
            if self.aliases.has_key(attr):
                decoded_attr = self.aliases[attr]
            else:
                decoded_attr = self.decode_attr(attr)
            encoded_attr = self.encode_attr(decoded_attr)
            if self._cache.has_key(attr):
                self._cache[attr] = self._cache[attr]
                if not self._cache.has_key(encoded_attr):
                    self._cache[encoded_attr] = self._cache[attr]
            attr_object = self.getattr(decoded_attr)
            if attr != encoded_attr:
                self._cache[attr] = attr_object
            self._cache[decoded_attr] = attr_object
            self._cache[encoded_attr] = attr_object
            return attr_object

        def __str__(self):
            raise NotImplementedError()

        def getattr(self, formatted_attr):
            raise NotImplementedError()

        def decode_attr(self, attr):
            raise NotImplementedError()
        
        def encode_attr(self, attr):
            raise NotImplementedError()
        
    class DBus(Wrapper):
        
        def __str__(self):
            return bus.__str__()

        def decode_attr(self, attr):
            return attr.replace('_', '.')

        def encode_attr(self, attr):
            return attr.replace('.', '_')

        def getattr(self, name):

            class DBusName(Wrapper):

                def __str__(self):
                    return name

                def decode_attr(self, attr):
                    return '/' + attr.replace('_', '/')

                def encode_attr(self, attr):
                    return attr[1:].replace('/', '_')

                def getattr(self, path):

                    dbus_object = bus.get_object(name, path)

                    class DBusObject(Wrapper):
                        
                        def __str__(self):
                            return path

                        def decode_attr(self, attr):
                            return attr.replace('_', '.')
                        
                        def encode_attr(self, attr):
                            return attr.replace('.', '_')
        
                        def subscribe(self, signal, handler, interface):
                            print dbus_object.connect_to_signal(signal, handler, self.resolve_attr(interface))
        
                        def getattr(self, interface):
                            return dbus.Interface(dbus_object, interface)

                    return DBusObject()

            return DBusName()

    return DBus()

if __name__ == "__main__":
    bus = _create(dbus.SystemBus())
    bus.aliases["ConsoleKit"] = "org.freedesktop.ConsoleKit"
    bus.ConsoleKit.aliases["Manager"] = "/org/freedesktop/ConsoleKit/Manager"
    bus.ConsoleKit.Manager.aliases["Main"] = "org.freedesktop.ConsoleKit.Manager"
    bus.ConsoleKit.Manager.aliases["Properties"] = "org.freedesktop.DBus.Properties"
    print bus.org_freedesktop_ConsoleKit.org_freedesktop_ConsoleKit_Manager.org_freedesktop_ConsoleKit_Manager.GetCurrentSession()
    bus.ConsoleKit.aliases["CurrentSession"] = bus.ConsoleKit.Manager.Main.GetCurrentSession()
    bus.ConsoleKit.CurrentSession.aliases["Main"] = "org.freedesktop.ConsoleKit.Session"
    print bus.ConsoleKit.CurrentSession.Main.GetUnixUser()
    print bus.ConsoleKit
    print bus.ConsoleKit.Manager
    print bus.ConsoleKit.Manager.Main
    print bus.ConsoleKit.Manager.Properties.GetAll("org.freedesktop.DBus.Properties")

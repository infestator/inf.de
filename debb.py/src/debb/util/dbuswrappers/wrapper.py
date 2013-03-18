import dbus
import dbus.mainloop.glib

__all__= ["system", "session"]

def _create(bus_factory):
    mainLoop = dbus.mainloop.glib.DBusGMainLoop()
    bus = bus_factory(mainloop=mainLoop)
    
    class Wrapper:

        def __init__(self, object=None):
            self._cache = {}
            self.aliases = {}
            self._object = object

        def resolve_attr(self, attr):
            if self._dict.has_key(attr):
                formatted_attr = self.aliases[attr]
            else:
                formatted_attr = self.decode_attr(attr)
            return formatted_attr

        def __getattr__(self, attr):
            try:
                self_attr = getattr(self._object, attr)
                if not isinstance(self_attr, dbus.proxies._DeferredMethod):
                    return self_attr
            except AttributeError:
                pass
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
        
        def __getitem__(self, item):
            return self.__getattr__(self.encode_attr(item))

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

        def list_names(self):
            return bus.list_names()

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
                            dbus_object.connect_to_signal(signal, handler, interface.__str__())
        
                        def getattr(self, interface):
                            object_interface = dbus.Interface(dbus_object, interface)
                            class DBusInterface:
                                
                                def __init__(self):
                                    self.converters = {}
                                
                                def __getattr__(self, attr):
                                    def handler(*args, **kwargs):
                                        result = getattr(object_interface, attr)(*args, **kwargs)
                                        if self.converters.has_key(attr):
                                            return self.converters[attr](result)
                                        else:
                                            return result
                                    return handler
                                
                                def __str__(self):
                                    return interface
                            
                            return DBusInterface()

                    return DBusObject(dbus_object)

            return DBusName()

    return DBus(bus)

system = _create(dbus.SystemBus)
session = _create(dbus.SessionBus)

import ipc
import shlex
import threading
import dbus

class DBusDaemon(dbus.service.Object):
    
    def __init__(self, address):
        pass

class Daemon(ipc.CommandServer):
    
    def __init__(self, address):
        class CommandListener(ipc.CommandListener):
            
            def __init__(self, daemon):
                ipc.CommandListener.__init__(self)
                self.__daemon = daemon
                
            def accept(self, command):
                argv = shlex.split(command)
                command = argv[0]
                func = getattr(self.__daemon, command)
                if len(argv) == 1:
                    func()
                else:
                    func(*(argv[1:]))
                #threading.Thread(target=getattr(self.__daemon, command), args=argv[1:]).start()
        
        ipc.CommandServer.__init__(self, address, CommandListener(self))

class Client:
    
    def __init__(self, address):
        self.__client = ipc.CommandClient(address)
    
    def __getattr__(self, name):
        def send(*argv):
            if len(argv) == 0:
                self.__client.send(name)
            else:
                self.__client.send(name + " '" + "' '".join(argv) + "'")
        return send

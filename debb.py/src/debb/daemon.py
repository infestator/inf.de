import ipc
import shlex
import threading

class Daemon(ipc.CommandServer):
    
    def __init__(self, address):
        class CommandListener(ipc.CommandListener):
            
            def __init__(self, daemon):
                ipc.CommandListener.__init__(self)
                self.__daemon = daemon
                
            def accept(self, command):
                argv = shlex.split(command)
                command = argv[0]
                #getattr(self.__daemon, command)(*argv[1:])
                threading.Thread(target=getattr(self.__daemon, command), args=argv[1:]).start()
                return None
        
        ipc.CommandServer.__init__(self, address, CommandListener(self))

class Client:
    
    def __init__(self, address):
        self.__client = ipc.CommandClient(address)
    
    def __getattr__(self, name):
        def send(*argv):
            self.__client.send(name + " '" + "' '".join(argv) + "'")
        return send

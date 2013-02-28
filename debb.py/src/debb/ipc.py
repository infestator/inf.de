import socket,os
import threading

class CommandServer(threading.Thread):
    
    def __init__(self, address, commandListener):
        if not isinstance(commandListener, CommandListener):
            raise TypeError
        self.__running = True
        self.__address = address
        threading.Thread.__init__(self)
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(address)
        s.listen(0)
        s.setblocking(True)
        self.__socket = s
        self.__commandListener = commandListener
        
    def run(self):
        while (self.__running):
            try:
                # TODO implement receiving commands with length more than 1k
                conn, _ = self.__socket.accept()
                if conn:
                    command = conn.recv(1024)
                    if not command:
                        continue
                    conn.close()
                    self.__commandListener.accept(command)
            except Exception as e:
                print e
        self.__socket.close()
            
    def stop(self):
        try:
            os.remove(self.__address)
        except:
            pass
        self.__running = False;

class CommandListener:
    
    def __init__(self):
        pass
    
    def accept(self, command):
        pass
    
class CommandClient:
    
    def __init__(self, address):
        s = socket.socket(socket.AF_UNIX)
        s.connect(address)
        self.__socket = s
        
    def send(self, command):
        self.__socket.send(command)

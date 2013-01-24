import socket,os
import threading

class CommandServer(threading.Thread):
    
    def __init__(self, address, commandListener):
        try:
            os.remove(address)
        except:
            pass
        self.__running = True
        threading.Thread.__init__(self)
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(address)
        s.listen(1)
        s.settimeout(0.1)
        self.__socket = s
        self.__commandListener = commandListener
        
    def run(self):
        while (self.__running):
            try:
                conn, _ = self.__socket.accept()
                if conn:
                    command = conn.recv(1024)
                    if not command:
                        continue
                    conn.close()
                    self.__commandListener.accept(command)
            except:
                pass  
        self.__socket.close()
            
    def stop(self):
        self.__running = False;

class CommandListener:
    
    def accept(self, command):
        pass
    
class CommandClient:
    
    def __init__(self, address):
        s = socket.socket(socket.AF_UNIX)
        s.connect(address)
        self.__socket = s
        
    def send(self, command):
        self.__socket.send(command)
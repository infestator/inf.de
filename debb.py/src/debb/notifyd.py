import ipc
import uuid
import daemon
import time

class NotifyDaemon(daemon.Daemon):
    
    def __init__(self, address):
        daemon.Daemon.__init__(self, address)
        self.__address = address
        
    def get_address(self):
        return self.__address
    
    def notify(self, message=None):
        print "Notified " + str(message)

def notify(address, *argv):
    client = ipc.CommandClient(address)
    client.send("'" + "' '".join(argv) + "'")

def start():
    #address = "/tmp/debb-notifyd-" + uuid.uuid4().get_hex()
    address = "/tmp/debb-notifyd"
    d = NotifyDaemon(address)
    d.start()
#    client = daemon.Client(address);
#    client.notify("Hello world!!!")
#    time.sleep(1)
#    client.stop()

if __name__ == "__main__":
    start()
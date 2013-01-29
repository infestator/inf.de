import socket
import os

socketFile = os.environ['HOME'] + '/appsocket'

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(socketFile)
s.send('Hello, world')
s.close()

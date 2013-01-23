import socket

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/tmp/socketname")
s.send('Hello, world')
s.close()

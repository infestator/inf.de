import socket, os
from inf.de.DEUtils import DEUtils

from inf.de.AppMenu import AppMenu

appMenu = AppMenu('/etc/xdg/menus/gnome-applications.menu', 'gnome')
DEUtils(appMenu).start()

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("/tmp/socketname")
except OSError:
    pass

s.bind("/tmp/socketname")
s.listen(1)
conn, addr = s.accept()
while 1:
    data = conn.recv(1024)
    if not data:
        break
    else:
        appMenu.popup(None, None, None, 0, 0)

conn.close()

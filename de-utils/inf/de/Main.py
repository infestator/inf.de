import os

from inf.de.DEUtils import DEUtils

from inf.de.AppMenu import AppMenu
from inf.de.IPC import CommandServer
from inf.de import IPC
import gtk

gtk.threads_init()

class Listener(IPC.CommandListener):
    
    def accept(self, command):
        gtk.threads_enter()
        appMenu.popup(None, None, None, 0, 0)
        gtk.threads_leave()

appMenu = AppMenu('/etc/xdg/menus/gnome-applications.menu', 'gnome')

socketFile = os.environ['HOME'] + '/appsocket'

try:
    os.remove(file)
except:
    pass

svr = CommandServer(socketFile, Listener())
svr.start()

DEUtils(appMenu)

gtk.threads_enter()
gtk.main()
gtk.threads_leave()

svr.stop()
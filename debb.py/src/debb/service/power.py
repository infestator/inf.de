import dbus.service
from debb.util import dbusfactory as dbusfactory_util
from debb.util import power as power_util
from debb.util import conf as conf_util
from gi.repository import GObject

from debb.util.dbuswrappers.wrapper import system  as dbus_system
from debb.util.dbuswrappers.wrapper import session as dbus_session

def start():

    util = power_util.create()
    settings = conf_util.create("debb.power-service")
        
    class Power(dbus.service.Object):
        pass
        
    def changed():
        if util.is_lid_closed():
            actions = {
                'none': lambda: None, 
                'suspend': util.suspend,
                'hibernate': util.hibernate,
                'poweroff': util.shutdown,
                'restart': util.restart
            }
            if util.is_on_battery():
                actions[settings['lid-close-action-battery']]()
            else:
                actions[settings['lid-close-action-ac']]()

    if any("debb.Power" == name for name in dbus_session.list_names()):
        print "Service is already running"
        return

    mainloop = GObject.MainLoop()

    dbus_session.request_name("debb.Power")
    Power(dbus_session, "/")
    util.connect_on_change_listener(changed)
    mainloop.run()

if __name__ == '__main__':
    start()

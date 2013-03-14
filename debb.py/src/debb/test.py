from debb.util.dbuswrappers import consolekit
from debb.util.dbuswrappers import upower
from debb.util.dbuswrappers import wrapper

if __name__ == "__main__":
    system_bus = wrapper.system
    
    def wrap_session(session):
        return session
    
#    system_bus.consolekit.manager.manager.converters["GetCurrentSession"]=lambda path: wrap_session(system_bus.consolekit[path])
#    system_bus.consolekit.manager.manager.add_path2object("GetCurrentSession")
    session = system_bus.consolekit.manager.manager.GetCurrentSession()
    print session.session.GetX11Display()
    system_bus
    print system_bus.upower.upower.upower.HibernateAllowed()
    print system_bus.upower.upower.properties.Get("org.freedesktop.UPower", "LidIsPresent")
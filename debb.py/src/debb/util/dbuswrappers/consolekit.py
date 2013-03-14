import wrapper

def _wrap_session(path):
    session = wrapper.system.consolekit[path]
    session.aliases["session"] = "org.freedesktop.ConsoleKit.Session"
    return session

wrapper.system.aliases["consolekit"] = "org.freedesktop.ConsoleKit" 
wrapper.system.consolekit.aliases = {
                                     "manager": "/org/freedesktop/ConsoleKit/Manager"
                                    }
wrapper.system.consolekit.manager.aliases = {
                                                "manager": "org.freedesktop.ConsoleKit.Manager"
                                               }
wrapper.system.consolekit.manager.manager.converters = {
                                                "GetCurrentSession": _wrap_session
                                                }


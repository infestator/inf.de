from debb.util import cli
from debb.util.dbus import wrapper
from debb.util.dbus import debb_session
import sys
if __name__ == "__main__":
    args = cli.parse_sysargv();
    for func in args:
        getattr(wrapper.session.session.session.session, func)(args[func])

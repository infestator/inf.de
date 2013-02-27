import os
import subprocess
import re
import shlex
import gtk
import gtk.gdk
from dbus import gobject_service
import gobject

__processes = list()

__path = os.environ['PATH'].split(os.pathsep)

r1 = re.compile('(?<!%)%[dDnNickvm]')
r2 = re.compile('%%')

class LaunchedProcess:
    
    def __init__(self, xdgEntry, process):
        self.__xdgEntry = xdgEntry
        self.__process = process
        
    def poll(self):
        return self.__process.poll()
    
    def wait(self):
        return self.__process.wait()
        
    def kill(self):
        self.__process.kill()

class Launcher(gtk.Builder):
    
    def __init__(self):
        gtk.Builder.__init__(self)
        print gtk.Builder.add_from_file(self, "../glade/launcher.glade")
        self.get_object("window1").show()

def get_processes():
    return __processes

def __parse_command(command, files=[], urls=[]):
    pieces = shlex.split(command)

    def substitute_single(pieces, index, values):
        i = index[0]
        n = len(values)
        if n == 1:
            pieces[i] = values[0]
        elif n == 0:
            pieces.remove(pieces[i])
            index[0] -= 1
        else:
            raise ValueError('Command is not supported')

    def substitute_multiple(pieces, index, values):
        i = index[0]
        n = len(values)
        if n > 0:
            pieces[i] = values
        elif n == 0:
            pieces.remove(pieces[i])
        else:
            raise ValueError('Command is not supported')

    pieces[0] = __locate(pieces[0])

    for i in range(len(pieces)):
        index = [i]
        if pieces[i] == '%f':
            substitute_single(pieces, index, files)
        elif pieces[i] == '%F':
            substitute_multiple(pieces, index, urls)
        elif pieces[i] == '%u':
            substitute_single(pieces, index, files)
        elif pieces[i] == '%U':
            substitute_multiple(pieces, index, urls)

    return pieces

def launch(desktop_entry, files=[], urls=[]):
    command_line = r1.sub('', desktop_entry.getExec())
    args = __parse_command(command_line, files, urls)
    process = subprocess.Popen(args)
    launched_process = LaunchedProcess(desktop_entry, process)
    __processes.append(launched_process)
    return launched_process

def kill_all():
    for launched_process in __processes:
        launched_process.kill()

def __locate(command):
    if os.path.exists(command):
        return command
    for path in __path:
        commandPath = path + os.sep + command
        if os.path.exists(commandPath):
            return commandPath
    raise Exception('Unable to find executable for ' + command)

processes = property(get_processes, None, None, None)

if __name__ == "__main__":
    launcher = Launcher()
    gtk.main()

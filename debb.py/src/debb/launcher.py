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

class Launcher(gtk.Window):
    
    def __init__(self):
        gtk.Window.__init__(self)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        gtk.Window.set_resizable(self, False)
        gtk.Window.set_type_hint(self, gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        
        result = gtk.Menu()
        result.show()

        buf = gtk.TextBuffer()
        buf.set_text(" ")
        input_ = gtk.TextView(buf)
        input_.show()
        model = gtk.ListStore(gobject.TYPE_STRING)
        results = gtk.TreeView()
        results.set_model(model)
        results.show()
        
        def update(search_string):
            model.append([search_string])
        
        def on_button_press(event):
            if event.keyval == gtk.keysyms.Return:
                input_.set_editable(False)
            elif event.keyval == gtk.keysyms.Escape:
                gtk.Window.emit(self, "delete-event", event)
            else:
                input_.set_editable(True)
                update(buf.get_text(buf.get_start_iter(), buf.get_end_iter()))
        
        input_.connect("key-press-event", lambda w, e: on_button_press(e))
        input_.connect("move-focus", lambda w, d: gtk.Window.emit(self, "delete-event", None))
        vpane = gtk.VPaned()
        vpane.add(input_)
        vpane.add(results)
        vpane.show()
        gtk.Window.add(self, vpane)
        gtk.Window.show(self)
        buf.set_text("")

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
    launcher.connect("delete-event", lambda w, x: gtk.main_quit())
    gtk.main()

import os
import subprocess

__processes = list()

__path = os.environ['PATH'].split(os.pathsep)

class LaunchedProcess:
    
    def __init__(self, xdgEntry, process):
        self.__xdgEntry = xdgEntry
        self.__process = process
        
    def kill(self):
        self.__process.kill()

def get_processes():
    return __processes

def launch(xdgEntry, command):
    if os.path.exists(command):
        process = subprocess.Popen(command)
    else:
        process = subprocess.Popen(__locate(command))
    launched_process = LaunchedProcess(xdgEntry, process)
    __processes.append(launched_process)
    return launched_process

def kill_all():
    for launched_process in __processes:
        launched_process.kill()

def __locate(command):
    for path in __path:
        commandPath = path + os.sep + command
        if os.path.exists(commandPath):
            return commandPath
    raise Exception('Unable to execute ' + command)

processes = property(get_processes, None, None, None)

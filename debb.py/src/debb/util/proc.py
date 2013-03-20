'''
Created on Mar 20, 2013

@author: abetaev
'''
import sys

def set_proc_name(name):
    if sys.platform == 'linux2':
        import ctypes
        libc = ctypes.cdll.LoadLibrary('libc.so.6')
        libc.prctl(16, name, 0, 0, 0)
    else:
        raise NotImplemented()

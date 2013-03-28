import sys
def parse(args):
    
    def parse_arg(arg):
        try:
            idx = arg.index('=')
            return arg[:idx], arg[idx+1:]
        except:
            return arg, True
    
    parsed = {}
    current = ""
    for arg in args:
        if arg.startswith("--"):
            current = arg[2:]
            if not parsed.has_key(current):
                parsed[current] = {}
        else:
            name, value = parse_arg(arg)
            parsed[current][name] = value
            
    return parsed

def parse_sysargv():
    return parse(sys.argv[1:])

def invoke(function, arguments):
    function(**arguments) 
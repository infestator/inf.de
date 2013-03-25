import dbus

def create():
    
    class util:

        pass
    
    return util()

if __name__ == "__main__":
    util = create()
    session = util.get_current_session()
    print session.GetUser()

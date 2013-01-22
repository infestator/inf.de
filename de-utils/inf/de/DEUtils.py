import threading
import gtk;
from inf.de.Config import Config
from inf.de.AppMenu import AppMenu

class DEUtils(threading.Thread):
    
    def __init__(self, menuFile):
        threading.Thread.__init__(self)
        config = Config()
        config.set_menu_file(menuFile)
        
        appMenu = AppMenu(config)
        
        statusIcon = gtk.StatusIcon()
        statusIcon.set_from_icon_name(appMenu.get_applications_icon())
        statusIcon.set_name("DEUtils");
        statusIcon.set_title('DEUtils')
        statusIcon.set_tooltip('DEUtils')
        statusIcon.set_visible(True)
        
        #utilsMenu = gtk.Menu();

        statusIcon.connect("activate", lambda x, y: self.show_applications_menu())
        #statusIcon.connect("popup-menu", lambda: self.show_utils_menu())
    
    def show_applications_menu(self):
        print 'apps'
        
    def show_utils_menu(self):
        print 'utils';
    
    def run(self):
        gtk.main();
    
    def stop(self):
        gtk.main_quit()
    

import threading
import gtk;
from inf.de.Config import Config
from inf.de.AppMenu import AppMenu

class DEUtils(threading.Thread):
    
    def __init__(self, menuFile, iconTheme):
        threading.Thread.__init__(self)
        config = Config()
        config.set_menu_file(menuFile)
        config.set_icon_theme(iconTheme)
        
        appMenu = AppMenu(config)
        
        statusIcon = gtk.status_icon_new_from_icon_name(appMenu.get_applications_icon())
        statusIcon.set_from_icon_name('applications-other')
        statusIcon.set_name("DEUtils");
        statusIcon.set_title('DEUtils')
        statusIcon.set_tooltip('DEUtils')
        statusIcon.set_visible(True)
        
        utilsMenu = gtk.Menu();
        exitItem= gtk.MenuItem("Quit")
        exitItem.connect("activate", lambda x: self.stop(appMenu))
        exitItem.show()
        utilsMenu.append(exitItem);

        def show_menu(menu, b = 0, t = 0):
            menu.popup(None, None, None, b, t)
            
        
        statusIcon.connect("activate", lambda x: show_menu(appMenu))
        statusIcon.connect("popup-menu", lambda x, b, t: show_menu(utilsMenu, b, t))
    
    def run(self):
        gtk.main();
    
    def stop(self, appMenu):
        appMenu.stop()
        gtk.main_quit()
    

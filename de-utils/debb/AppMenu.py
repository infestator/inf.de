import gtk
import xdg.IconTheme
import xdg.Menu
import Launcher
import re

class AppMenu(gtk.Menu):

    def __init__(self, menu_file, icon_theme):
        gtk.Menu.__init__(self)
        
        r1 = re.compile('(?<!%)%[fFuUdDnNickvm]')
        r2 = re.compile('%%')

        def traverseXDGMenu(xdgEntry):
            def createMenuItem(label, iconName):
                iconPath = xdg.IconTheme.getIconPath(iconName, None, icon_theme)
                if iconPath is not None:
                    iconSource = gtk.IconSource()
                    iconSource.set_filename (iconPath)
                    iconSet = gtk.IconSet()
                    iconSet.add_source(iconSource)
                    scaled = iconSet.render_icon(gtk.Style(), gtk.TEXT_DIR_LTR, gtk.STATE_NORMAL, gtk.ICON_SIZE_LARGE_TOOLBAR, None, None)
                    menuItem = gtk.ImageMenuItem()
                    img = gtk.image_new_from_pixbuf(scaled)
                    menuItem.set_image(img)
                else:
                    menuItem = gtk.MenuItem()
                menuItem.set_label(label)
                return menuItem
            
            if isinstance(xdgEntry, xdg.Menu.MenuEntry):
                item = createMenuItem(xdgEntry.DesktopEntry.getName(), xdgEntry.DesktopEntry.getIcon())
                command = r2.sub('%', r1.sub('', xdgEntry.DesktopEntry.getExec())).rstrip()
                item.connect("activate", lambda menuItem, command: Launcher.launch(xdgEntry, command), command)
            elif isinstance(xdgEntry, xdg.Menu.Menu):
                item = createMenuItem(xdgEntry.getName(), xdgEntry.getIcon())
                menu = gtk.Menu()
                item.set_submenu(menu);
                print xdgEntry.getName()
                for xdgMenuEntry in xdgEntry.getEntries():
                    menu.append(traverseXDGMenu(xdgMenuEntry))
            elif isinstance(xdgEntry, xdg.Menu.Separator):
                item = gtk.SeparatorMenuItem()
            item.show()
            return item
        
        xdgMenu = xdg.Menu.parse(menu_file);
        for xdgMenuEntry in xdgMenu.getEntries():
            item = traverseXDGMenu(xdgMenuEntry)
            self.append(item)
        
        self.__applications_icon = xdgMenu.getIcon();
        self.show()
        
        def tray_activate_callback():
            self.menu.popup(None, None, None, 0, 0)
            
        def tray_menu_callback():
            pass
        
    def get_applications_icon(self):
        return self.__applications_icon

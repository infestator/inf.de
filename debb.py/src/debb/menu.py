import gtk
import xdg.IconTheme
import xdg.Menu
import launcher

class Menu(gtk.Menu):

    def __init__(self, menu_file=None, icon_theme=None):
        gtk.Menu.__init__(self)
        
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
                desktop_entry = xdgEntry.DesktopEntry
                item = createMenuItem(desktop_entry.getName(), desktop_entry.getIcon())
                item.connect("activate", lambda w: launcher.launch(desktop_entry))
            elif isinstance(xdgEntry, xdg.Menu.Menu):
                item = createMenuItem(xdgEntry.getName(), xdgEntry.getIcon())
                menu = gtk.Menu()
                item.set_submenu(menu);
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
        
    def get_applications_icon(self):
        return self.__applications_icon

def merge_menu_entries(xdg_menu_entry, xdg_menu_entry_addon):
    if not isinstance(xdg_menu_entry, xdg.Menu.MenuEntry):
        raise TypeError(xdg_menu_entry + " is not xdg.Menu.MenuEntry type")
    if not isinstance(xdg_menu_entry_addon, xdg.Menu.MenuEntry):
        raise TypeError(xdg_menu_entry_addon + " is not xdg.Menu.MenuEntry type")

if __name__ == "__main__":
    menu = Menu("/etc/xdg/menus/gnome-applications.menu", "gnome")
    menu.connect("hide", lambda w: gtk.main_quit())
    menu.popup(None, None, None, 0, 0)
    gtk.main()

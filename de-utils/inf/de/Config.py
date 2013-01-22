class Config:

    def get_icon_theme(self):
        return self.__iconTheme


    def get_menu_file(self):
        return self.__menuFile


    def set_icon_theme(self, value):
        self.__iconTheme = value


    def set_menu_file(self, value):
        self.__menuFile = value


    def del_icon_theme(self):
        del self.__iconTheme


    def del_menu_file(self):
        del self.__menuFile

    
    __iconTheme = None
    
    __menuFile = None
    
    iconTheme = property(get_icon_theme, set_icon_theme, del_icon_theme, "")
    menuFile = property(get_menu_file, set_menu_file, del_menu_file, "")

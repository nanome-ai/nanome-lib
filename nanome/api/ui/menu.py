from nanome._internal._ui import _Menu
from .io import MenuIO

class Menu(_Menu):
    io = MenuIO()
    def __init__(self):
        _Menu.__init__(self)
        self.io = MenuIO(self)
    
    def register_closed_callback(self, func):
        self._closed_callback = func

    def register_opened_callback(self, func):
        self._opened_callback = func

    #region properties
    @property
    def root(self):
        return self._root
    
    @root.setter
    def root(self, value):
        self._root = value

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
    #endregion
    @classmethod
    def get_plugin_menu(cls):
        return _Menu._get_plugin_menu()
    @classmethod
    def set_plugin_menu(cls, menu):
        _Menu._set_plugin_menu(menu)

    def find_content(self, content_id):
        return self._find_content(content_id)

    def get_all_content(self):
        return self._get_all_content()

    def get_all_nodes(self):
        return self._get_all_nodes()

Menu.io._setup_addon(Menu)
_Menu._create = Menu
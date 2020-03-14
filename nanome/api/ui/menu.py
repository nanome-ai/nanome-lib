from nanome._internal._ui import _Menu
from .io import MenuIO

class Menu(_Menu):
    io = MenuIO()
    def __init__(self, index = 0, title = "title"):
        _Menu.__init__(self, index, title)
        self.io = MenuIO(self)
    
    def register_closed_callback(self, func):
        self._closed_callback = func

    #region properties
    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if type(value) is not str:
            value = str(value)
        self._title = value

    @property
    def locked(self):
        return self._locked
    
    @locked.setter
    def locked(self, value):
        self._locked = value

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

    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, value):
        self._index = value
    #endregion

    def find_content(self, content_id):
        return self._find_content(content_id)

    def get_all_content(self):
        return self._get_all_content()

    def get_all_nodes(self):
        return self._get_all_nodes()

Menu.io._setup_addon(Menu)
_Menu._create = Menu
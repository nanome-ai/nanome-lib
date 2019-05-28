from nanome.util import Vector3
from . import _LayoutNode

class _Menu(object):
    _menu = None

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self, title = "title"):
        #Protocol
        self.enabled = True
        self._id = 0
        self.title = title
        self.locked = False
        self._width = 0.7
        self._height = 0.6
        #self.all_layout_nodes[]
        #self.all_contents[]

        #API
        self._root = _LayoutNode._create()
        self._opened_callback = lambda self: None
        self._closed_callback = lambda self: None

#region callback
    def _on_closed_callback (self):
        self._closed_callback(self)

    def _on_opened_callback (self):
        self._opened_callback(self)

#endregion

    @classmethod
    def _get_plugin_menu(cls):
        if (_Menu._menu is None):
            _Menu._menu = _Menu._create()
        return _Menu._menu

    @classmethod
    def _set_plugin_menu(cls, val):
        _Menu._menu = val

    def _find_content(self, content_id):
        return self._root._find_content(content_id)

    def _get_all_content(self):
        all_content = []
        self._root._append_all_content(all_content)
        return all_content

    def _get_all_nodes(self):
        all_nodes = []
        self._root._append_all_nodes(all_nodes)
        return all_nodes

    def _copy_data(self, other):
        self.enabled = other.enabled
        self.title = other.title
        self.locked = other.locked
        self._width = other.width
        self._height = other.height


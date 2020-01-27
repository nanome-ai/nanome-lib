from nanome.util import Vector3
from . import _LayoutNode

class _Menu(object):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self, index = 0, title = "title"):
        #Protocol
        self._enabled = True
        self._title = title
        self._locked = False
        self._width = 0.7
        self._height = 0.6
        self._index = index
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
        self._enabled = other._enabled
        self._title = other._title
        self._locked = other._locked
        self._width = other._width
        self._height = other._height
        self._index = other._index


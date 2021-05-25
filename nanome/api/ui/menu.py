from nanome._internal._ui import _Menu
from .io import MenuIO


class Menu(_Menu):
    """
    | Represents a menu for a plugin
    """
    io = MenuIO()

    def __init__(self, index=0, title="title"):
        _Menu.__init__(self, index, title)
        self.io = MenuIO(self)

    def register_closed_callback(self, func):
        """
        | Registers a function to be called when the menu's close button is pressed.

        :param func: called the menu is closed
        :type func: method (:class:`~nanome.ui.Menu`) -> None
        """
        self._closed_callback = func

    # region properties
    @property
    def enabled(self):
        """
        | Determines the visibility of the menu

        :type: :class:`bool`
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def title(self):
        """
        | The title which appears at the top of the menu

        :type: :class:`str`
        """
        return self._title

    @title.setter
    def title(self, value):
        if type(value) is not str:
            value = str(value)
        self._title = value

    @property
    def locked(self):
        """
        | Whether or not the menu is locked in place

        :type: :class:`bool`
        """
        return self._locked

    @locked.setter
    def locked(self, value):
        self._locked = value

    @property
    def root(self):
        """
        | The hierarchical root LayoutNode of the menu

        :type: :class:`~nanome.ui.LayoutNode`
        """
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    @property
    def width(self):
        """
        | The width of the menu

        :type: :class:`float`
        """
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """
        | The height of the menu

        :type: :class:`float`
        """
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def index(self):
        """
        | The index of the menu.
        | Used to determine a menu's identity.
        | Menus with the same index will replace one another when updated.

        :type: :class:`int`
        """
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
    # endregion

    def find_content(self, content_id):
        """
        | Finds a piece of content by its content ID.

        :param content_id: the ID of the content to find
        :type content_id: :class:`int`
        :return: The UI content on this menu matching the ID
        :rtype: :class:`~nanome.ui.UIBase`
        """
        return self._find_content(content_id)

    def get_all_content(self):
        """
        | Gets all content from this menu

        :return: A list of all UI content on this menu
        :rtype: :class:`list` <:class:`~nanome.ui.UIBase`>
        """
        return self._get_all_content()

    def get_all_nodes(self):
        """
        | Gets all LayoutNodes from this menu

        :return: A list of all LayoutNodes on this menu
        :rtype: :class:`list` <:class:`~nanome.ui.LayoutNode`>
        """
        return self._get_all_nodes()


Menu.io._setup_addon(Menu)
_Menu._create = Menu
